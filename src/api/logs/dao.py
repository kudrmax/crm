from sqlalchemy import select

from src.api.contacts.models import MContact
from src.api.dao_base import DAO
from src.api.logs.models import MLog
from src.api.logs.schemas import SLogCreate, SEmptyLogCreate
from src.errors import *


class DAOLog(DAO):
    model = MLog

    async def _get_one_or_none_contact_by_name(self, name: str) -> MContact:
        query = select(MContact).where(MContact.name == name)
        contact = await self.db.execute(query)
        contact = contact.scalar_one_or_none()
        return contact

    async def create(self, log_create: SLogCreate):
        contact = await self._get_one_or_none_contact_by_name(log_create.name)
        if not contact:
            raise ContactNotFoundError
        m_log = MLog(contact_id=contact.id, log=log_create.log)
        # m_log.datetime = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        self.db.add(m_log)
        await self.db.commit()
        await self.db.refresh(m_log)
        return m_log

    async def get_all_by_name(self, name):
        query = select(MContact).where(MContact.name == name)
        contact = await self.db.execute(query)
        contact = contact.scalar_one_or_none()
        if not contact:
            raise ContactNotFoundError
        contact_id = contact.id
        return await self.get_all_with_filter(contact_id=contact_id)

    async def create_empty_log(self, empty_log: SEmptyLogCreate):
        return await self.create(
            SLogCreate(
                name=empty_log.name,
                log="",
            )
        )

    async def delete(self, log_id):
        m_log = await self.get_one_or_none_with_filter(id=log_id)
        if not m_log:
            return None
        await self.db.delete(m_log)
        await self.db.commit()
        return m_log
