from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.contacts.models import MContact
from src.api.contacts.schemas import SContactCreate, SContactUpdate
from src.api.dao_base import DAO
from src.database import get_db


class DAOContact(DAO):
    model = MContact

    async def create(self, s_contact_create: SContactCreate) -> MContact:
        m_contact = MContact(**s_contact_create.model_dump(exclude_unset=True))
        try:
            self.db.add(m_contact)
            await self.db.commit()
            return m_contact
        except IntegrityError as e:
            raise HTTPException(status_code=500, detail=e)

    async def delete(self, id: UUID) -> MContact | None:
        query = select(MContact).where(MContact.id == id)
        m_contact = (await self.db.execute(query)).scalar_one_or_none()
        if not m_contact:
            return None
        await self.db.delete(m_contact)
        await self.db.commit()
        return m_contact

    async def update(self, id: int, update_contact: SContactUpdate):
        query = select(MContact).where(MContact.id == id)
        m_contact = (await self.db.execute(query)).scalar_one_or_none()
        if not m_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        for key, val in update_contact.model_dump(exclude_unset=True).items():
            setattr(m_contact, key, val)
        await self.db.commit()
        return m_contact
