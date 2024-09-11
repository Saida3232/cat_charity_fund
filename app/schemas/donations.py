from typing import Optional

from pydantic import PositiveInt

from .base import BaseDb, BaseDbFull, BaseUpdate


class DonationCreate(BaseUpdate):
    """field optional comment, full_amount"""
    comment: Optional[str]


class DonationUpdate(DonationCreate):
    """field optional comment, optional full_amount"""
    full_amount: Optional[PositiveInt]


class DonationDbForUser(DonationCreate, BaseDb):
    pass


class DonationDB(DonationCreate, BaseDbFull):
    user_id: int
