from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from app.crud.projects import charifyproject_crud
from app.models import CharityProject
from app.schemas.projects import CharityProjectSchemaUpdate


async def check_project_exist(project_id: int,
                              session: AsyncSession) -> CharityProject:
    project = await charifyproject_crud.get(project_id, session)
    if project is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail='Проект не найден!')
    return project


async def check_name_duplicate(
        project_name: str, session: AsyncSession) -> None:
    room_id = await charifyproject_crud.get_project_id_by_name(
        project_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


def validate_full_amount(obj_data: CharityProjectSchemaUpdate,
                         project: CharityProject):
    if obj_data.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Нельзя установить сумму меньше внесенной'
            f' - {project.full_amount}')