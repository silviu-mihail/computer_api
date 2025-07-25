from hashlib import sha256
from authentication_repository import AuthenticationRepository
from jwt_service.jwt_model import create_jwt, validate_jwt
from auth_logger import logger


class AuthenticationService:
    def __init__(self):
        self._repository = AuthenticationRepository()

    async def register(self, data):
        logger.info('Register service called')

        hashed_password = sha256(data.password.encode('utf-8')).hexdigest()
        try:
            await self._repository.insert_user(data.email, hashed_password)
        except Exception as e:
            logger.error('User already exists in the database')
            raise Exception('User already exists') from e

    async def login(self, data):
        logger.info('Login service called')

        user_data = await self._repository.get_user(data.email)
        hashed_password = sha256(data.password.encode('utf-8')).hexdigest()

        if user_data is None:
            logger.error('User was not found')
            raise Exception("User not found")

        if user_data.password == hashed_password:
            logger.info('Creating the JWT token')
            return create_jwt(user_data.id, user_data.email)
        else:
            logger.error('Wrong credentials - authentication failed')
            raise ValueError('The passwords do not match')

    async def validate(self, data):
        logger.info('Token validation service called')

        try:
            jwt_data = validate_jwt(data.token)

            user_data = await self._repository.get_user(jwt_data['email'])
            if user_data is None:
                logger.error('Invalid JWT token claims')
                return 'Invalid JWT token', False

            return 'Token is valid', True
        except Exception:
            logger.error('Invalid JWT token')
            return 'Invalid JWT token', False
