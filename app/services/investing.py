from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def close_project(target: Union[CharityProject, Donation]):
    target.fully_invested = True
    target.invested_amount = target.full_amount
    target.close_date = datetime.now()
    return target


def invest(
        target: Union[CharityProject, Donation],
        sources: Union[CharityProject, Donation],
):
    money = target.full_amount - target.invested_amount
    money_2 = sources.full_amount - sources.invested_amount

    if money > money_2:
        target.invested_amount += money_2
        close_project(sources)
    elif money == money_2:
        close_project(sources)
        close_project(target)
    else:
        sources.invested_amount += money
        close_project(target)
    return target, sources


async def investing_to(
        target: Union[CharityProject, Donation],
        sources: Union[CharityProject, Donation],
        session: AsyncSession
):
    investing_models = await session.execute(select(sources).where(
        sources.fully_invested == 0).order_by(sources.create_date))
    investing_models = investing_models.scalars().all()
    for model in investing_models:
        target, model = invest(target, model)
        session.add(target)
        session.add(model)

    await session.commit()
    await session.refresh(target)
    return target
