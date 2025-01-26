import datetime as dt
from typing import List

from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError

from src.models.log.models import MLog, MLogCreate, MLogUpdate
from src.storage.postgres.connection.engine import engine
from src.storage.postgres.repositories.contacts.errors import ContactNotFoundErr
from src.storage.postgres.repositories.logs.errors import ContactIdNotFoundErr


class LogRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_all(self) -> List[MLog]:
        with self.engine.connect() as conn:
            query = text('''SELECT * FROM logs''')
            rows = conn.execute(query).all()
            return self.__convert_rows_to_models(rows)

    def get_by_id(self, id: int) -> MLog | None:
        with self.engine.connect() as conn:
            query = text('''SELECT * FROM contacts WHERE id = :id''')
            rows = conn.execute(query, {'id': id}).all()
            if len(rows) == 0:
                return None
            return self.__convert_row_to_model(rows[0])

    def create(self, new_log: MLogCreate) -> bool:
        with self.engine.connect() as conn:
            try:
                query = text(
                    '''INSERT INTO logs (contact_id, datetime, text) VALUES (:contact_id, :datetime, :text)'''
                )
                rows = conn.execute(query, {
                    'contact_id': new_log.contact_id,
                    'datetime': new_log.datetime if new_log.datetime is not None else dt.datetime.now(),
                    'text': new_log.text if new_log.text is not None else '',
                })
                conn.commit()
                return bool(rows.rowcount)
            except IntegrityError as e:
                if 'on table "logs" violates foreign key constraint' in str(e):
                    raise ContactIdNotFoundErr()

    def update_by_id(self, id: int, new_log_data: MLogUpdate) -> bool:
        with self.engine.connect() as conn:
            try:
                query = text('''
                        UPDATE logs
                        SET 
                            contact_id = COALESCE(:contact_id, contact_id), 
                            datetime = COALESCE(:datetime, datetime), 
                            text = COALESCE(:text, text)
                        WHERE id = :id
                    ''')
                rows = conn.execute(query, {
                    'id': id,
                    'contact_id': new_log_data.contact_id,
                    'datetime': new_log_data.datetime,
                    'text': new_log_data.text,
                })
                conn.commit()
                return bool(rows.rowcount)
            except IntegrityError as e:
                if 'on table "logs" violates foreign key constraint' in str(e):
                    raise ContactIdNotFoundErr()

    def delete_by_id(self, id: int) -> bool:
        with self.engine.connect() as conn:
            query = text('''DELETE FROM logs WHERE id = :id''')
            rows = conn.execute(query, {'id': id})
            conn.commit()
            return bool(rows.rowcount)

    @staticmethod
    def __convert_row_to_model(row) -> MLog:
        return MLog(*row)

    @staticmethod
    def __convert_rows_to_models(rows) -> List[MLog]:
        return [MLog(*row) for row in rows]


r = LogRepository(engine=engine)

print(r.get_all())
r.delete_by_id(9)
print(r.get_all())