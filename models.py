# models.py
from pydantic import BaseModel, Field


class PowRequest(BaseModel):
    base: float
    exponent: float


class FibRequest(BaseModel):
    n: int = Field(ge=0)


class FactRequest(BaseModel):
    n: int = Field(ge=0)
