from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class BaseUpdate(BaseModel):
    """field full_amount"""
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class BaseDb(BaseUpdate):
    """fields id,create_date,full_amount"""
    id: int
    create_date: datetime

    class Config():
        orm_mode = True


class BaseDbFull(BaseDb):
    """fields id,create_date,fully_invested, invested_amount,close_date"""
    fully_invested: bool
    close_date: Optional[datetime]
    invested_amount: int
