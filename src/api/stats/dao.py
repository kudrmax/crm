from typing import List

from sqlalchemy import select, func, distinct, String, cast

from src.api.contacts.models import MContact
from src.api.dao_base import DAO
from src.api.logs.models import MLog
from src.api.stats.schemas import SDayCount


class DAOStats(DAO):
    async def get_stat_count_of_interactions(self, name: str | None = None) -> List[SDayCount] | SDayCount:
        SQL = """
        SELECT 
            logs.contact_id AS contact_id,
            contacts.name AS name, 
            COUNT(DISTINCT DATE(datetime)) AS day_count
        FROM contacts
        JOIN logs
            ON contacts.id = logs.contact_id
        GROUP BY logs.contact_id;
        """
        query = (
            select(
                MLog.contact_id.label('contact_id'),
                MContact.name.label('name'),
                func.count(distinct(func.date(MLog.datetime))).label('day_count')
            )
            .join(MContact, MContact.id == MLog.contact_id)
            .group_by(MLog.contact_id, MContact.name)
        )
        rows = (await self.db.execute(query)).all()
        data = [SDayCount(name=row[1], day_count=row[2]) for row in rows]
        # if name:
        #     for name, day_count in data:
        #         if name == name:
        #             return SDayCount(name=name, day_count=day_count)
        #     return SDayCount(name=name, day_count=-1)

        return data

    async def get_days_count_since_last_interaction(self, name: str | None = None) -> List[SDayCount] | SDayCount:
        SQL = """
        SELECT 
            logs.contact_id AS contact_id,
            contacts.name AS name,
            DATE_PART('day', CURRENT_DATE - MAX(DATE(logs.datetime))) AS days_since_last_interaction
        FROM contacts
        JOIN logs ON contacts.id = logs.contact_id
        GROUP BY logs.contact_id, contacts.name;
        """
        query = (
            select(
                MLog.contact_id.label('contact_id'),
                MContact.name.label('name'),
                func.date_part(
                    'day',
                    func.age(func.current_date(), func.max(func.date(MLog.datetime)))
                ).label('days_since_last_interaction')
            )
            .join(MContact, MContact.id == MLog.contact_id)
            .group_by(MLog.contact_id, MContact.name)
        )
        rows = (await self.db.execute(query)).all()
        return [SDayCount(name=row[1], day_count=row[2]) for row in rows]
