import os
import datetime
import jwt as pyjwt
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class TokenPayload(BaseModel):
    sub: str
    email: str
    exp: datetime.datetime
    iat: datetime.datetime

def create_jwt(user_id, email):
    payload = TokenPayload(
        sub=str(user_id),
        email=email,
        exp=datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
        iat=datetime.datetime.now(datetime.UTC)
    )

    return pyjwt.encode(payload.model_dump(), os.getenv("SECRET_KEY"), algorithm="HS256")

def validate_jwt(token):
    try:
        decoded_payload = pyjwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"]
        )

        payload = TokenPayload(**decoded_payload)

        return {
            "sub": payload.sub,
            "email": payload.email
        }

    except pyjwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except pyjwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")
