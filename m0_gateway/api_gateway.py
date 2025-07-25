import httpx
import os
import json
from flask import Flask, request, jsonify
from response import ResponseModel
from pathlib import Path
from dotenv import load_dotenv
from shared.logger import setup_logger
from shared.telemetry import init_telemetry


api_gateway = Flask(__name__)
init_telemetry(api_gateway,
               service_name='gateway',
               trace_file='gateway_traces.jsonl')
logger = setup_logger(service_name='gateway', log_file='gateway_log.jsonl')


env_path = Path(__file__).parent / '.env'
load_env = load_dotenv(dotenv_path=env_path)


SERVICE_MAP = {
    'authenticator': os.getenv('AUTHENTICATOR_URL'),
    'calculator': os.getenv('CALCULATOR_URL')
}


def create_output_model(status_code, message, content, headers):
    return ResponseModel(
        status_code=status_code, message=message,
        content=content, headers=headers
    )


async def auth_validate(token):
    if not token:
        logger.warning('JWT token not found')

        return 'Missing JWT token', False

    if not token.startswith('Bearer '):
        logger.warning('Invalid JWT token')

        return 'Invalid JWT format', False

    jwt = token.split(' ')[1]

    async with httpx.AsyncClient() as client:
        logger.info('Calling authorization service to validate the JWT token')

        validation_response = await client.request(
            method='POST',
            url=os.getenv('VALIDATION_URL'),
            headers={'Content-Type': 'application/json'},
            content=json.dumps({'token': jwt}).encode('utf-8')
        )

    json_format = validation_response.json()

    return json_format['message'], json_format['status']


@api_gateway.route('/api/<service>/<path:endpoint>', methods=['POST'])
async def proxy(service, endpoint):
    logger.info(f'API Gateway called for service: {service}')

    if service == 'calculator':
        logger.info('Checking authorization header')

        message, status = await auth_validate(
            request.headers.get('Authorization')
        )
        if not status:
            logger.info('Wrong JWT token credentials or expired')

            return jsonify(create_output_model(
                status_code=401,
                message=message,
                content=None,
                headers={}
            ).model_dump()), 401

    base_url = SERVICE_MAP.get(service)
    if not base_url:
        logger.warning(f'Unknown service called: {service}')

        return jsonify(create_output_model(
            status_code=404,
            message='Unknown service',
            content={'error': f'Unknown service: {service}'},
            headers={}
        ).model_dump()), 404

    target_url = f'{base_url}/{service}/{endpoint}'

    logger.info(f'Calling endpoint: {target_url}')

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={key: value for (key, value) in request.headers
                         if key.lower() != 'host'},
                params=request.args,
                content=request.get_data()
            )
        except httpx.RequestError as e:
            logger.error(f"Service at endpoint {target_url} was unreachable")

            return jsonify(create_output_model(
                status_code=502,
                message='Service unreachable',
                content={
                    'error': str(e)
                },
                headers={}
            ).model_dump()), 502

    try:
        content = response.json()
    except ValueError:
        logger.error("Endpoint returned incorrect output")

        return jsonify(create_output_model(
            status_code=500,
            message='Incorrect microservice output',
            content=None,
            headers={}
        ).model_dump()), 500

    logger.info("Endpoint call ran successfully")

    return jsonify(create_output_model(
        status_code=response.status_code,
        message=content.pop('message'),
        content=content,
        headers=response.headers
    ).model_dump()), response.status_code


if __name__ == '__main__':
    logger.info('Started service API Gateway')
    api_gateway.run(port=os.getenv('GATEWAY_PORT'))
