from typing import List, Dict
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

    async def get_log(self, contact_id: UUID) -> str:
        query = select(MContact).where(MContact.id == contact_id)
        m_contact = (await self.db.execute(query)).scalar_one_or_none()
        if not m_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return m_contact.log if m_contact.log else ""

    async def add_data_to_log(self, contact_id: UUID, log_data: str) -> Dict[str, str]:
        query = select(MContact).where(MContact.id == contact_id)
        m_contact = (await self.db.execute(query)).scalar_one_or_none()
        if not m_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        log = m_contact.log if m_contact.log else ""
        new_log = log + '\n' + log_data if log != "" else log_data
        setattr(m_contact, 'log', new_log)
        await self.db.commit()
        return {
            'old_log': log,
            'new_log': new_log,
            'log_data': log_data
        }
