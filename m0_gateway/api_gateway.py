from flask import Flask, request, jsonify
import requests


api_gateway = Flask(__name__)


AUTHENTICATION_URL = 'http://localhost:5001'
CALCULATOR_URL     = 'http://localhost:5002'


@api_gateway.route('/api/authenticator/<path:endpoint>', methods=['GET'])
def proxy_to_authenticator(endpoint):
    response = requests.request(
        method = request.method,
        url = f'{AUTHENTICATION_URL}/authenticator/{endpoint}',
        headers = {key: value for (key, value) in request.headers if key != 'Host'},
        data = request.get_data(),
        cookies = request.cookies,
        allow_redirects = False
    )

    return (response.content, response.status_code, response.headers.items())


@api_gateway.route('/api/calculator/<path:endpoint>', methods=['GET'])
def proxy_to_calculator(endpoint):
    response = requests.request(
        method = request.method,
        url = f'{CALCULATOR_URL}/calculator/{endpoint}',
        headers = {key: value for (key, value) in request.headers if key != 'Host'},
        data = request.get_data(),
        cookies = request.cookies,
        allow_redirects = False
    )

    return (response.content, response.status_code, response.headers.items())


if __name__ == '__main__':
    api_gateway.run(port=5000)
