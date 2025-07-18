import httpx
from flask import Flask, request, jsonify


api_gateway = Flask(__name__)

SERVICE_MAP = {
    'authenticator': 'http://localhost:5001',
    'calculator': 'http://localhost:5002'
}


@api_gateway.route('/api/<service>/<path:endpoint>', methods=['GET', 'POST', 'PUT'])
async def proxy(service, endpoint):
    base_url = SERVICE_MAP.get(service)
    if not base_url:
        return {'error': f'Unknown service: {service}'}, 404
    
    target_url = f'{base_url}/{service}/{endpoint}'

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers={key: value for (key, value) in request.headers if key.lower() != 'host'},
                params=request.args,
                content=request.get_data(),
                cookies=request.cookies
            )
        except httpx.RequestError as e:
            return {"error": f'Service unreachable: {str(e)}'}, 502
        
    return response.content, response.status_code, dict(response.headers)


if __name__ == '__main__':
    api_gateway.run(port=5000)
