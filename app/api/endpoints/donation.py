from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donations import donations_crud
from app.models import CharityProject, User
from app.schemas.donations import DonationCreate, DonationDB, DonationDbForUser
from app.services.investing import investing_to

router = APIRouter()


@router.get('/',
            response_model=list[DonationDB],
            dependencies=[Depends(current_superuser)]
            )
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    projects = await donations_crud.multi_get(session)
    return projects


@router.get('/my',
            response_model=list[DonationDbForUser],
            dependencies=[Depends(current_user)]
            )
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donations_crud.get_by_user(user.id, session)
    return donations


@router.post('/',
             response_model=DonationDbForUser,
             dependencies=[Depends(current_user)]
             )
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donat = await donations_crud.create(donation, session, user)
    return await investing_to(donat, CharityProject, session)
