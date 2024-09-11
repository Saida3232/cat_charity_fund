from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


def close_project(obj: Union[CharityProject, Donation]):
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()
    return obj


def invest(
        obj: Union[CharityProject, Donation],
        obj_2: Union[CharityProject, Donation],
):
    money = obj.full_amount - obj.invested_amount
    money_2 = obj_2.full_amount - obj_2.invested_amount

    if money > money_2:
        obj.invested_amount += money_2
        close_project(obj_2)
    elif money == money_2:
        close_project(obj_2)
        close_project(obj)
    else:
        obj_2.invested_amount += money
        close_project(obj)
    return obj, obj_2


async def investing_to(
        obj: Union[CharityProject, Donation],
        obj_2: Union[CharityProject, Donation],
        session: AsyncSession
):
    investing_models = await session.execute(select(obj_2).where(
        obj_2.fully_invested == 0).order_by(obj_2.create_date))
    investing_models = investing_models.scalars().all()
    for model in investing_models:
        obj, model = invest(obj, model)
        session.add(obj)
        session.add(model)

    await session.commit()
    await session.refresh(obj)
    return obj
