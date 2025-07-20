from dataclasses import field

from pydantic import BaseModel, validator, field_validator
from typing import ClassVar


class CalculatorResponse(BaseModel):
    message: str
    result: int


class PowRequest(BaseModel):
    base: int
    exponent: int

    @field_validator("exponent")
    def exponent_should_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Exponent must be non-negative.")
        return v


class FibRequest(BaseModel):
    number: int

    @field_validator("number")
    def number_should_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Fibonacci index must be non-negative.")
        return v


class FactRequest(BaseModel):
    n: int

    @field_validator("n")
    def n_should_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Factorial input must be non-negative.")
        return v
