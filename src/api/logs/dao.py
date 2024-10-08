from collections import defaultdict
import datetime
from typing import List, Dict

from sqlalchemy import select, Date, desc, func

from src.api.contacts.models import MContact
from src.api.dao_base import DAO
from src.api.logs.models import MLog
from src.api.logs.schemas import SLogCreate, SEmptyLogCreate, SLogUpdate, SLogRead
from src.errors import LogNotFoundError, ContactNotFoundError


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

    async def create(self, log_create: SLogCreate, date: datetime.date | None = None):
        new_datetime = None
        if date:
            query = select(MLog).filter(MLog.datetime.cast(Date) == date).order_by(desc(MLog.datetime))
            last_log = await self.db.execute(query)
            last_log = last_log.scalar()
            if last_log:
                new_datetime = last_log.datetime + datetime.timedelta(microseconds=1)
            else:
                new_datetime = datetime.datetime.combine(date, datetime.time(0, 1))
        contact = await self._get_contact_by_name(log_create.name)
        if new_datetime:
            m_log = MLog(contact_id=contact.id, log=log_create.log, datetime=new_datetime)
        else:
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
        numbers_to_log_id_dict: Dict[int, int] = {}
        number = 1
        for data in result_list:
            for log in data['logs']:
                log.number = number
                numbers_to_log_id_dict[int(log.number)] = log.id
                number += 1
        return {
            'numbers_to_log_id': numbers_to_log_id_dict,
            'data': result_list,
        }

    async def create_empty_log(self, empty_log: SEmptyLogCreate):
        return await self.create(
            SLogCreate(
                name=empty_log.name,
                log="",
            )
        )

    async def edit_log_by_id(self, log_id, log_update: SLogUpdate):
        m_log = await self.get_one_or_none_by_id(log_id)
        if not m_log:
            raise LogNotFoundError
        if log_update.log:
            setattr(m_log, 'log', log_update.log)
        if log_update.datetime:
            setattr(m_log, 'datetime', log_update.datetime)
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

    async def edit_log_date_by_id(self, log_id: int, date: datetime.date):
        query = select(MLog).filter(MLog.datetime.cast(Date) == date).order_by(desc(MLog.datetime))
        last_log = await self.db.execute(query)
        last_log = last_log.scalar()
        if last_log:
            new_datetime = last_log.datetime + datetime.timedelta(microseconds=1)
        else:
            new_datetime = datetime.datetime.combine(date, datetime.time(0, 1))
        log = await self.get_one_by_id(log_id)
        setattr(log, 'datetime', new_datetime)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    async def get_last_logs(self, days_count: int = 5):
        recent_date = datetime.date.today() - datetime.timedelta(days=days_count)

        logs_query = (
            select(MLog.contact_id, func.date(MLog.datetime).label('log_date'), MLog.log).
            filter(MLog.datetime.cast(Date) >= recent_date).
            order_by(MLog.contact_id, MLog.datetime)
        )
        logs_data = await self.db.execute(logs_query)

        result = {}
        for contact_id, log_date, log in logs_data:
            if not log or log == "":
                continue
            contact = (await self.db.execute(select(MContact).where(MContact.id == contact_id))).scalar_one_or_none()
            contact_name = contact.name
            if contact_name:
                if contact_name not in result:
                    result[contact_name] = {}
                if log_date not in result[contact_name]:
                    result[contact_name][log_date] = []
                result[contact_name][log_date].append(log)

        return result

    async def get_log_by_log_id(self, log_id: int):
        query = select(MLog).where(MLog.id == log_id)
        log_data = await self.db.execute(query)
        log_data = log_data.scalar_one_or_none()
        if not log_data:
            raise LogNotFoundError
        return log_data
