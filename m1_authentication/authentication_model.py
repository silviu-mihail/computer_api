from pydantic import BaseModel, Field


class AuthenticationModel(BaseModel):
    id: int
    email: str = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., max_length=100)