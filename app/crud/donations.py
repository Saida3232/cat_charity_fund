from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.models import Donation


class CrudDonation(CrudBase):
    async def get_by_user(
            self,
            user_id: int,
            session: AsyncSession
    ):
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id))
        return donations.scalars().all()


donations_crud = CrudDonation(Donation)