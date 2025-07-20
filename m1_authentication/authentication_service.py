from hashlib import sha256
from authentication_repository import AuthenticationRepository
from jwt_service.jwt_model import create_jwt, validate_jwt

class AuthenticationService:
    def __init__(self):
        self._repository = AuthenticationRepository()

    async def register(self, data):
        hashed_password = sha256(data.password.encode('utf-8')).hexdigest()
        try:
            await self._repository.insert_user(data.email, hashed_password)
        except Exception as e:
            print(e)
            raise Exception('User already exists') from e

    async def login(self, data):
        user_data = await self._repository.get_user(data.email)
        hashed_password = sha256(data.password.encode('utf-8')).hexdigest()

        if user_data is None:
            raise Exception("User not found")

        if user_data.password == hashed_password:
            return create_jwt(user_data.id, user_data.email)
        else:
            raise ValueError('The passwords do not match')

    async def validate(self, data):
        try:
            jwt_data = validate_jwt(data.token)

            user_data = await self._repository.get_user(jwt_data['email'])
            if user_data is None:
                return 'Invalid JWT token', False

            return 'Token is valid', True
        except Exception as e:
            print(e)
            return 'Invalid JWT token', False