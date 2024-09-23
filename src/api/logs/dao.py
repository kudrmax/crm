from collections import defaultdict
from datetime import datetime
from typing import List, Dict

from sqlalchemy import select

from src.api.contacts.models import MContact
from src.api.dao_base import DAO
from src.api.logs.models import MLog
from src.api.logs.schemas import SLogCreate, SEmptyLogCreate, SLogUpdate, SLogRead
from src.errors import *


class DAOLog(DAO):
    model = MLog

    async def _get_one_or_none_contact_by_name(self, name: str) -> MContact:
        query = select(MContact).where(MContact.name == name)
        contact = await self.db.execute(query)
        contact = contact.scalar_one_or_none()
        return contact

    async def _get_contact_by_name(self, name: str) -> MContact:
        contact = await self._get_one_or_none_contact_by_name(name)
        if not contact:
            raise ContactNotFoundError
        return contact

    async def create(self, log_create: SLogCreate):
        contact = await self._get_contact_by_name(log_create.name)
        m_log = MLog(contact_id=contact.id, log=log_create.log)
        self.db.add(m_log)
        await self.db.commit()
        await self.db.refresh(m_log)
        return m_log

    async def get_all_logs_by_name(self, name):
        contact = await self._get_contact_by_name(name)
        return await self.get_all_with_filter(contact_id=contact.id)

    async def get_all_logs_grouped_by_date(self, name: str):
        logs: List[MLog] = await self.get_all_logs_by_name(name)

        result_dict: Dict[str, List[SLogRead]] = defaultdict(list)
        for log in logs:
            log_str = log.log
            if log_str == "" or log_str is None:
                continue
            log_datetime = log.datetime
            result_dict[log_datetime.date().strftime("%Y-%m-%d")].append(SLogRead(
                id=log.id,
                contact_id=log.contact_id,
                datetime=log.datetime,
                log=log.log
            ))
        result_list = []
        dates_sorted = sorted(list(result_dict.keys()))
        for date in dates_sorted:
            result_list.append({
                'date': date,
                'logs': sorted(result_dict[date], key=lambda x: x.datetime)
            })
        number = 1
        for data in result_list:
            for log in data['logs']:
                log.number = number
                number += 1
        return result_list

    async def create_empty_log(self, empty_log: SEmptyLogCreate):
        return await self.create(
            SLogCreate(
                name=empty_log.name,
                log="",
            )
        )

    async def edit_log_by_id(self, log_id, log_update: SLogUpdate):
        m_log = self.get_one_or_none_by_id(log_id)
        if not m_log:
            raise LogNotFoundError
        if log_update.log:
            setattr(m_log, 'log', log_update.log)
        # if log_update.date:
        #     я хочу взять все логи с MLog.contact_id == m_log.contact_id, потом из этих логов взять логи, с датой равной дате MLog.datetime (учти что MLog.datetime содержит и дату и время, а меня интересует только дата)
        #     и потом если такой лог нашелся, то поставить для данного лога (m_log) дату равную log_update.date, а время через 5 секунд после времени того лога, который мы нашли
        #     query = select(MLog).where(MLog.contact_id == m_log.contact_id).where(MLog.datetime.date)
        #     pass
        await self.db.commit()
        await self.db.refresh(m_log)
        return m_log

    async def delete(self, log_id):
        m_log = await self.get_one_or_none_with_filter(id=log_id)
        if not m_log:
            return None
        await self.db.delete(m_log)
        await self.db.commit()
        return m_log
