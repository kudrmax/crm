from typing import List, Optional
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.contacts.models import MContact
from src.api.contacts.schemas import SContactCreate, SContactUpdate
from src.database import get_db


class DAO:
    model = None

    def __init__(self, db=Depends(get_db)):
        self.db: AsyncSession = db

    async def get_all(self) -> List[model]:
        query = select(self.model)
        return list((await self.db.execute(query)).scalars().all())

    async def get_one_or_none(self, id: UUID) -> Optional[model]:
        query = select(self.model).where(self.model.id == id)
        return (await self.db.execute(query)).scalar_one_or_none()
