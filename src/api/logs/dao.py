from typing import Dict
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.api.contacts.dao import DAOContact
from src.api.contacts.models import MContact
from src.api.dao_base import DAO
from src.api.logs.models import MLog
from src.api.logs.schemas import SLogCreate


class DAOLog(DAO):
    model = MLog

    async def create(self, log_create: SLogCreate):
        m_log = MLog(**log_create.model_dump(exclude_unset=True))
        try:
            self.db.add(m_log)
            await self.db.flush()
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail=f'Не удолось добавить лог: {log_create.model_dump(exclude_unset=True)}'
            )
        else:
            await self.db.commit()
            return m_log

# class DAOLog(DAOContact):
#     model = MContact
#
#     # async def _extract_data_from_str_log(self, log_data: str) -> Tuple[str, list] | None:
#     #     lines = log_data.strip().split("\n")
#     #     if len(lines) < 2:
#     #         return None
#     #     name = lines[0].strip()
#     #     data = [s.strip() for s in lines[1:]]
#     #     return name, data
#     #
#     # async def _add_str_to_log(self, old_log: str, log_data: str):
#     #     name, data = self._extract_data_from_str_log(log_data)
#     #     old_log = "\n".join([old_log, data])
#
#     async def get_log(self, contact_id: UUID) -> str:
#         m_contact = await self.get_one_by_id(contact_id)
#         return m_contact.log if m_contact.log else ""
#
#     async def add_data_to_log(self, contact_id: UUID, log_data: SLogData) -> Dict[str, str]:
#         date_str = log_data.date.strftime('%Y-%m-%d')
#         log_str = log_data.log_str
#
#         m_contact = await self.get_one_by_id(contact_id)
#         old_log = m_contact.log
#         lines = old_log.split("\n")
#         for i, line in enumerate(lines):
#             if line.startswith(date_str):
#                 lines.insert(i + 1, f'- {log_str}')
#                 break
#         else:
#             lines.append(date_str)
#             lines.append(f'- {log_str}')
#         new_log = '\n'.join(lines)
#         setattr(m_contact, 'log', new_log)
#         await self.db.commit()
#         return {
#             'old_log': old_log,
#             'new_log': m_contact.log,
#         }
#
#     async def replace_log(self, contact_id: UUID, new_log: str) -> Dict[str, str]:
#         m_contact = await self.get_one_by_id(contact_id)
#         old_log = m_contact.log
#         setattr(m_contact, 'log', new_log)
#         await self.db.commit()
#         return {
#             'old_log': old_log,
#             'new_log': m_contact.log,
#         }
#
#     async def remove_log(self, contact_id: UUID) -> Dict[str, str]:
#         return await self.replace_log(contact_id, "")
