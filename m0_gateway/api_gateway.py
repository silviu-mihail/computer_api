import httpx
import os
import json
from flask import Flask, request, jsonify
from response import ResponseModel
from pathlib import Path
from dotenv import load_dotenv


api_gateway = Flask(__name__)


env_path = Path(__file__).parent / '.env'
load_env = load_dotenv(dotenv_path=env_path)


SERVICE_MAP = {
    'authenticator': os.getenv('AUTHENTICATOR_URL'),
    'calculator': os.getenv('CALCULATOR_URL')
}


def create_output_model(status_code, message, content, headers):
    return ResponseModel(
        status_code=status_code, message=message, content=content, headers=headers
    )


async def auth_validate(token):
    if not token:
        return 'Missing JWT token', False

    if not token.startswith('Bearer '):
        return 'Invalid JWT format', False

    jwt = token.split(' ')[1]

    async with httpx.AsyncClient() as client:
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
    if service == 'calculator':
        message, status = await auth_validate(request.headers.get('Authorization'))
        if not status:
            return jsonify(create_output_model(
                status_code=401,
                message=message,
                content=None,
                headers={}
            ).model_dump()), 401

    base_url = SERVICE_MAP.get(service)
    if not base_url:
        return jsonify(create_output_model(
            status_code=404,
            message='Unknown service',
            content={'error': f'Unknown service: {service}'},
            headers={}
        ).model_dump()), 404
    
    target_url = f'{base_url}/{service}/{endpoint}'

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={key: value for (key, value) in request.headers if key.lower() != 'host'},
                params=request.args,
                content=request.get_data()
            )
        except httpx.RequestError as e:
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
        return jsonify(create_output_model(
            status_code=500,
            message='Incorrect microservice output',
            content=None,
            headers={}
        ).model_dump()), 500

    return jsonify(create_output_model(
        status_code=response.status_code,
        message=content.pop('message'),
        content=content,
        headers=response.headers
    ).model_dump()), response.status_code


if __name__ == '__main__':
    api_gateway.run(port=os.getenv('GATEWAY_PORT'))
