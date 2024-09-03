import asyncio
import datetime
from typing import List, Dict, Tuple
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
        m_contact = await self.get_one_or_none_by_id(id)
        if not m_contact:
            return None
        await self.db.delete(m_contact)
        await self.db.commit()
        return m_contact

    async def update(self, id: int, update_contact: SContactUpdate):
        m_contact = await self.get_one_by_id(id)
        for key, val in update_contact.model_dump(exclude_unset=True).items():
            setattr(m_contact, key, val)
        await self.db.commit()
        return m_contact

    # async def _extract_data_from_str_log(self, log_data: str) -> Tuple[str, list] | None:
    #     lines = log_data.strip().split("\n")
    #     if len(lines) < 2:
    #         return None
    #     name = lines[0].strip()
    #     data = [s.strip() for s in lines[1:]]
    #     return name, data
    #
    # async def _add_str_to_log(self, old_log: str, log_data: str):
    #     name, data = self._extract_data_from_str_log(log_data)
    #     old_log = "\n".join([old_log, data])

    async def get_log(self, contact_id: UUID) -> str:
        m_contact = await self.get_one_by_id(contact_id)
        return m_contact.log if m_contact.log else ""

    async def add_data_to_log(self, contact_id: UUID, log_data: str) -> Dict[str, str]:
        m_contact = await self.get_one_by_id(contact_id)
        old_log = m_contact.log
        new_log = old_log + '\n' + log_data if old_log != "" else log_data
        setattr(m_contact, 'log', new_log)
        await self.db.commit()
        return {
            'old_log': old_log,
            'new_log': m_contact.log,
            'log_data': log_data
        }

    async def replace_log(self, contact_id: UUID, new_log: str) -> Dict[str, str]:
        m_contact = await self.get_one_by_id(contact_id)
        old_log = m_contact.log
        setattr(m_contact, 'log', new_log)
        await self.db.commit()
        return {
            'old_log': old_log,
            'new_log': m_contact.log,
        }

    async def remove_log(self, contact_id: UUID) -> Dict[str, str]:
        return await self.replace_log(contact_id, "")

# async def main():
#     with open('log_data.txt', 'r') as f:
#         log_data = f.read()
#     dao = DAOContact()
#     res = await dao._extract_data_from_str_log(log_data)
#     print(res)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
