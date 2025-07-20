import os
from flask import Flask, jsonify, request
from pathlib import Path
from dotenv import load_dotenv
from pydantic import ValidationError

from authentication_service import AuthenticationService
from dtos import AuthenticationRequest, AuthenticationResponse, ValidateTokenRequest, ValidateTokenResponse

authenticator_app = Flask(__name__)

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

authenticator_service = AuthenticationService()

@authenticator_app.route('/authenticator/register', methods=['POST'])
async def register():
    try:
        data = AuthenticationRequest.model_validate(request.get_json())
    except ValidationError:
        return jsonify(AuthenticationResponse(
            message="JSON validation failed",
            content=None
        ).model_dump()), 400

    try:
        await authenticator_service.register(data)
    except Exception:
        return jsonify(AuthenticationResponse(
            message="User already exists",
            content=None
        ).model_dump()), 409

    return jsonify(AuthenticationResponse(
        message='Account created successfully',
        content=None
    ).model_dump()), 200

@authenticator_app.route('/authenticator/login', methods=['POST'])
async def login():
    try:
        data = AuthenticationRequest.model_validate(request.get_json())
    except ValidationError:
        return jsonify(AuthenticationResponse(
            message="JSON validation failed",
            content=None
        ).model_dump()), 400

    try:
        token = await authenticator_service.login(data)
    except ValueError:
        return jsonify(AuthenticationResponse(
            message="Wrong credentials",
            content=None
        ).model_dump()), 401
    except Exception:
        return jsonify(AuthenticationResponse(
            message="User not found",
            content=None
        ).model_dump()), 404

    return jsonify(AuthenticationResponse(
        message='Login was successful',
        content=token
    ).model_dump()), 200

@authenticator_app.route('/authenticator/validate', methods=['POST'])
async def validate():
    data = ValidateTokenRequest.model_validate(request.get_json())

    message, status = await authenticator_service.validate(data)

    return jsonify(ValidateTokenResponse(
        message=message, status=status
    ).model_dump()), 200

if __name__ == '__main__':
    authenticator_app.run(port=int(os.getenv('AUTHENTICATOR_PORT', 5000)))
