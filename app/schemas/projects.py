from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from .base import BaseDbFull, BaseUpdate


class CharityProjectSchemaCreate(BaseUpdate):
    """change name, description, full_amount"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)


class CharityProjectSchemaUpdate(BaseModel):
    """change name, description, full_amount"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    @validator('name')
    def validate_name(cls, value: str):
        if value.isspace() or value is None:
            raise ValueError('Поле не может быть пустым')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectSchemaDb(BaseDbFull, CharityProjectSchemaCreate):
    pass