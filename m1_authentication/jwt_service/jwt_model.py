import os
import datetime
import jwt as pyjwt
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class TokenPayload(BaseModel):
    sub: int
    email: str
    exp: datetime.datetime
    iat: datetime.datetime

def create_jwt(user_id, email):
    payload = TokenPayload(
        sub=user_id,
        email=email,
        exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
        iat=datetime.datetime.now(datetime.UTC)
    )

    return pyjwt.encode(payload.model_dump(), os.getenv("SECRET_KEY"), algorithm="HS256")
