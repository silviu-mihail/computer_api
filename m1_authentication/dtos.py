from pydantic import BaseModel, Field
from typing import Any


class AuthenticationRequest(BaseModel):
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., max_length=32)


class AuthenticationResponse(BaseModel):
    message: str
    content: Any