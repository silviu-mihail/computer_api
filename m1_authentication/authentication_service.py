from hashlib import sha256
from authentication_repository import AuthenticationRepository


class AuthenticationService:
    def __init__(self):
        self._repository = AuthenticationRepository()

    async def register(self, data):
        hashed_password = sha256(data.password.encode('utf-8')).hexdigest()

        try:
            await self._repository.insert_user(data.email, hashed_password)
        except Exception as e:
            raise Exception('User already exists') from e