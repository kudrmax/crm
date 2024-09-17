from sqlalchemy import select

from src.api.contacts.models import MContact
from src.api.dao_base import DAO
from src.api.logs.models import MLog
from src.api.logs.schemas import SLogCreate
from src.errors import ContactNotFoundError


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

    async def create_empty_log(self, name: str):
        return await self.create(
            SLogCreate(
                name=name,
                log="",
            )
        )
