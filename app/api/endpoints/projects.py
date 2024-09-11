from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_name_duplicate, check_project_exist,
                                validate_full_amount)
from app.core.db import get_async_session
from app.core.users import current_superuser
from app.crud.projects import charifyproject_crud
from app.models import Donation
from app.schemas.projects import (CharityProjectSchemaCreate,
                                  CharityProjectSchemaDb,
                                  CharityProjectSchemaUpdate)
from app.services.investing import investing_to

router = APIRouter()


@router.get('/', response_model=list[CharityProjectSchemaDb])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    projects = await charifyproject_crud.multi_get(session)
    return projects


@router.post('/',
             response_model=CharityProjectSchemaDb,
             dependencies=[Depends(current_superuser)])
async def create_project(
    project: CharityProjectSchemaCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charifyproject_crud.create(project, session)
    return await investing_to(new_project, Donation, session)


@router.patch('/{project_id}',
              response_model=CharityProjectSchemaDb,
              dependencies=[Depends(current_superuser)]
              )
async def partially_update_project(
    project_id: int,
    obj_data: CharityProjectSchemaUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exist(project_id, session)

    if project.fully_invested:
        raise HTTPException(status_code=400, detail='Проект уже закрыт!')

    if obj_data.name is not None:
        await check_name_duplicate(obj_data.name, session)

    if obj_data.full_amount is not None:
        validate_full_amount(obj_data, project)

    project = await charifyproject_crud.update(project, obj_data, session)
    return project


@router.delete('/{project_id}',
               response_model=CharityProjectSchemaDb,
               dependencies=[Depends(current_superuser)]
               )
async def delete_project(project_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    project = await check_project_exist(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В фонд уже внесли деньги, его нельзя закрыть.')
    project = await charifyproject_crud.remove(project, session)
    return project
