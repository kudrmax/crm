from typing import List

from sqlalchemy import select, func, distinct

from src.api.contacts.models import MContact
from src.api.dao_base import DAO
from src.api.logs.models import MLog
from src.api.stats.schemas import SDayCount


class DAOStats(DAO):
    async def get_stat_count_of_interasions(self) -> List[SDayCount]:
        SQL = """
        SELECT clogs.contact_id AS contact_id, contacts.name AS name, COUNT(DISTINCT DATE(datetime)) AS day_count
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
        return [SDayCount(name=row[1], day_count=row[2]) for row in rows]
