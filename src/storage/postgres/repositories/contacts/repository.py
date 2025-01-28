from typing import List

from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError

from src.models.contact.model import MContactCreate, MContact, MContactUpdate
from src.errors import ContactNotFoundErr, ContactAlreadyExistsErr
from src.storage.postgres.connection.engine import engine


class ContactRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_all(self) -> List[MContact]:
        with self.engine.connect() as conn:
            query = text('''SELECT * FROM contacts''')
            rows = conn.execute(query).all()
            return self.__convert_rows_to_models(rows)

    def get_by_name(self, name: str) -> MContact | None:
        with self.engine.connect() as conn:
            query = text('''SELECT * FROM contacts WHERE name = :name''')
            rows = conn.execute(query, {'name': name}).all()
            if len(rows) == 0:
                return None
            return self.__convert_row_to_model(rows[0])

    def get_by_contact_ids(self, contact_ids: List[int]) -> List[MContact]:
        if len(contact_ids) == 0:
            return []
        with self.engine.connect() as conn:
            query = text('''SELECT * FROM contacts WHERE id IN :contact_ids''')
            rows = conn.execute(query, {'contact_ids': tuple(contact_ids)}).all()
            return self.__convert_rows_to_models(rows)

    def create(self, new_contact: MContactCreate) -> bool:
        with self.engine.connect() as conn:
            try:
                query = text(
                    '''INSERT INTO contacts (name, phone, telegram, birthday) VALUES (:name, :phone, :telegram, :birthday)'''
                )
                rows = conn.execute(query, {
                    'name': new_contact.name,
                    'phone': new_contact.phone,
                    'telegram': new_contact.telegram,
                    'birthday': new_contact.birthday,
                })
                conn.commit()
                return bool(rows.rowcount)
            except IntegrityError as e:
                if 'duplicate key value violates unique constraint' in str(e):
                    raise ContactAlreadyExistsErr()

    def update_by_name(self, old_name: str, new_contact_data: MContactUpdate) -> bool:
        new_contact_data.telegram = self.__prepare_telegram(new_contact_data.telegram)

        with self.engine.connect() as conn:
            try:
                query = text('''
                    UPDATE contacts
                    SET 
                        name = COALESCE(:name, name), 
                        phone = COALESCE(:phone, phone), 
                        telegram = COALESCE(:telegram, telegram), 
                        birthday = COALESCE(:birthday, birthday)
                    WHERE name = :old_name
                ''')
                rows = conn.execute(query, {
                    'old_name': old_name,
                    'name': new_contact_data.name,
                    'phone': new_contact_data.phone,
                    'telegram': new_contact_data.telegram,
                    'birthday': new_contact_data.birthday,
                })
                conn.commit()
                return bool(rows.rowcount)
            except ContactNotFoundErr as e:
                raise  # TODO проверить как выглядит эта ошибка
            except IntegrityError as e:
                if 'duplicate key value violates unique constraint' in str(e):
                    raise ContactAlreadyExistsErr()

    def delete_by_name(self, name: str) -> bool:
        with self.engine.connect() as conn:
            query = text('''DELETE FROM contacts WHERE name = :name''')
            rows = conn.execute(query, {'name': name})
            conn.commit()
            return bool(rows.rowcount)

    @staticmethod
    def __convert_row_to_model(row) -> MContact:
        return MContact(*row)

    @staticmethod
    def __convert_rows_to_models(rows) -> List[MContact]:
        return [MContact(*row) for row in rows]

    @staticmethod
    def __prepare_telegram(telegram: str) -> str:
        return telegram[1:] if ((len(telegram) > 0) and telegram[0] == '@') else telegram
