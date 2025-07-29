import os
from flask import Flask, jsonify, request
from pathlib import Path
from dotenv import load_dotenv
from pydantic import ValidationError

from authentication_service import AuthenticationService
from dtos import (
    AuthenticationRequest,
    AuthenticationResponse,
    ValidateTokenRequest,
    ValidateTokenResponse
)
from shared.telemetry import init_telemetry
from auth_logger import logger

authenticator_app = Flask(__name__)
init_telemetry(authenticator_app,
               service_name='authenticator',
               trace_file='authenticator_traces.jsonl')


env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


authenticator_service = AuthenticationService()


@authenticator_app.route('/authenticator/register', methods=['POST'])
async def register():
    logger.info("Register endpoint has been called")

    try:
        logger.info('Validating register request JSON')

        data = AuthenticationRequest.model_validate(request.get_json())
    except ValidationError:
        logger.error('Invalid JSON request')

        return jsonify(AuthenticationResponse(
            message="JSON validation failed",
            content=None
        ).model_dump()), 400

    try:
        logger.info('Calling the registration service')

        await authenticator_service.register(data)
    except Exception:
        logger.error(f'User already exists with the given credentials: '
                     f'{data.email}')

        return jsonify(AuthenticationResponse(
            message="User already exists",
            content=None
        ).model_dump()), 409

    logger.info('Register operation ran successfully')

    return jsonify(AuthenticationResponse(
        message='Account created successfully',
        content=None
    ).model_dump()), 200


@authenticator_app.route('/authenticator/login', methods=['POST'])
async def login():
    logger.info('Login endpoint has been called')

    try:
        logger.info('Validating login request JSON')

        data = AuthenticationRequest.model_validate(request.get_json())
    except ValidationError:
        logger.error('Invalid JSON request')

        return jsonify(AuthenticationResponse(
            message="JSON validation failed",
            content=None
        ).model_dump()), 400

    try:
        logger.info('Calling the login service')

        token = await authenticator_service.login(data)
    except ValueError:
        logger.error(f'The given credentials are wrong: {data.email}')

        return jsonify(AuthenticationResponse(
            message="Wrong credentials",
            content=None
        ).model_dump()), 401
    except Exception:
        logger.error(f'The user with the email {data.email} does not exists')

        return jsonify(AuthenticationResponse(
            message="User not found",
            content=None
        ).model_dump()), 404

    logger.info('Login operation ran successfully')

    return jsonify(AuthenticationResponse(
        message='Login was successful',
        content=token
    ).model_dump()), 200


@authenticator_app.route('/authenticator/validate', methods=['POST'])
async def validate():
    logger.info('JWT validation endpoint has been called')

    data = ValidateTokenRequest.model_validate(request.get_json())

    logger.info('Validating JWT token')

    message, status = await authenticator_service.validate(data)

    logger.info('Validation operation ran successfully')

    return jsonify(ValidateTokenResponse(
        message=message, status=status
    ).model_dump()), 200

if __name__ == '__main__':
    logger.info('Started service authenticator')

    authenticator_app.run(port=int(os.getenv('AUTHENTICATOR_PORT', 5000)))
