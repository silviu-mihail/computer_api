from pydantic import BaseModel, Field
from typing import Any, Dict


class ResponseModel(BaseModel):
    status: int = Field(..., alias='status_code')
    message: str
    content: Any
    headers: Dict[str, str]

    class Config:
        allow_population_by_field_name = True
