import os
import jwt
import datetime
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class TokenPayload(BaseModel):
    sub: int
    email: str
    exp: datetime.datetime
    iat: datetime.datetime


def create_jwt(user_id, email):
    user_payload = TokenPayload(
        sub=user_id,
        email=email,
        exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
        iat=datetime.datetime.now(datetime.UTC)
    )

    token = jwt.encode(user_payload.model_dump(), os.getenv('SECRET_KEY'), algorithm="HS256")
    return token
