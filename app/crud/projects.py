from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.models import CharityProject


class CharityProjectCrud(CrudBase):
    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name)
        )
        return db_project_id.scalars().first()


charifyproject_crud = CharityProjectCrud(CharityProject)