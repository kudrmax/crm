import difflib
from typing import List

from src.api.contacts.models import MContact
from src.api.contacts.schemas import SContactCreate, SContactUpdate
from src.api.dao_base import DAO
from src.api.errors.errors import *


class DAOContact(DAO):
    model = MContact

    async def get_contact(self, name: str) -> MContact:
        contact = await self.get_one_or_none_with_filter(name=name)
        if not contact:
            raise ContactNotFoundError(name=name)
        return contact

    async def create(self, s_contact_create: SContactCreate) -> MContact:
        m_contact = MContact(**s_contact_create.model_dump(exclude_unset=True))
        if await self.get_one_or_none_with_filter(name=s_contact_create.name):
            raise ContactAlreadyExistsError(name=s_contact_create.name)
        self.db.add(m_contact)
        await self.db.commit()
        await self.db.refresh(m_contact)
        return m_contact

    async def delete(self, name: str) -> MContact | None:
        m_contact = await self.get_one_or_none_with_filter(name=name)
        if not m_contact:
            return None
        await self.db.delete(m_contact)
        await self.db.commit()
        return m_contact

    async def update(self, name: str, update_contact: SContactUpdate) -> MContact:
        if update_contact.name:
            if await self.get_one_or_none_with_filter(name=update_contact.name):
                raise ContactAlreadyExistsError(name=update_contact.name)
        m_contact = await self.get_one_or_none_with_filter(name=name)
        if not m_contact:
            raise ContactNotFoundError(name=name)
        for key, val in update_contact.model_dump(exclude_unset=True).items():
            setattr(m_contact, key, val)
        await self.db.commit()
        await self.db.refresh(m_contact)
        return m_contact

    async def search(self, name: str, name_count: int = 3) -> List[MContact]:
        m_contacts = await self.get_all()
        names = [contact.name.lower() for contact in m_contacts]
        close_names = difflib.get_close_matches(name.lower(), names, n=name_count)
        return [contact for contact in m_contacts if contact.name.lower() in close_names]
