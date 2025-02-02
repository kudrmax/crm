import dataclasses
import difflib
from typing import List, Tuple, Any

from src.models.contact.model import MContact, MContactCreate, MContactUpdate
from src.models.log.models import MLogUpdate, MLog, MLogCreate, MLogWithNumbers
from src.storage.postgres.connection.engine import engine
from src.errors import ContactNotFoundErr, ContactAlreadyExistsErr
from src.storage.postgres.repositories.contacts.repository import ContactRepository
from src.storage.postgres.repositories.logs.repository import LogRepository


class ContactLogService:
    def __init__(self, contact_repository: ContactRepository, log_repository: LogRepository):
        self.contact_repository = contact_repository
        self.log_repository = log_repository

    # GET

    def get_all_contacts(self) -> List[MContact]:
        return self.contact_repository.get_all()

    def get_contact_by_name(self, name: str) -> MContact | None:
        return self.contact_repository.get_by_name(name)

    def get_contact_id_by_name(self, name: str) -> int | None:
        contact = self.get_contact_by_name(name)
        if not contact:
            return None
        return contact.id

    def get_last_contacts(self) -> List[MContact]:
        ids, last_dates = self.log_repository.get_last_contact_ids()
        id_to_last_date_dict = {id: last_date for id, last_date in zip(ids, last_dates)}

        contacts = self.contact_repository.get_by_contact_ids(ids)
        contacts = sorted(contacts, key=lambda c: id_to_last_date_dict[c.id], reverse=True)

        return contacts

    def get_logs_by_contact_name(self, name: str, need_numbers: bool = False) -> List[MLog] | List[MLogWithNumbers]:
        contact = self.contact_repository.get_by_name(name)
        logs = self.log_repository.get_by_contact_id(contact.id)
        if not need_numbers:
            return logs

        logs = sorted(logs, key=lambda l: l.datetime)
        logs_with_numbers = [
            MLogWithNumbers(*dataclasses.astuple(logs[i]), i + 1)
            for i in range(len(logs))
        ]
        return logs_with_numbers

    def get_similar_contacts(self, name: str, name_count: int = 6) -> List[MContact]:
        # TODO улучшить функцию
        contacts = self.get_all_contacts()
        names = [contact.name.lower() for contact in contacts]
        close_names = difflib.get_close_matches(name.lower(), names, n=name_count)
        return [contact for contact in contacts if contact.name.lower() in close_names]

    # CREATE

    def create_contact(self, contact: MContactCreate) -> bool:
        try:
            return self.contact_repository.create(contact)
        except ContactAlreadyExistsErr:
            raise ContactAlreadyExistsErr()

    def create_log(self, log_create: MLogCreate) -> bool:
        return self.log_repository.create(log_create)

    # UPDATE

    def update_contact_by_name(self, name: str, new_contact: MContactUpdate) -> bool:
        return self.contact_repository.update_by_name(name, new_contact)

    def update_log_by_log_id(self, log_id: int, log_update: MLogUpdate) -> bool:
        return self.log_repository.update_by_id(log_id, log_update)

    # DELETE

    def delete_contact_by_name(self, name: str) -> bool:
        return self.contact_repository.delete_by_name(name)

    def delete_log_by_log_id(self, id: int) -> bool:
        return self.log_repository.delete_by_id(id)

    # OTHER

    @staticmethod
    def get_names_from_models(contacts: List[MContact]) -> List[str]:
        return [contact.name for contact in contacts]


def new_contact_service() -> ContactLogService:
    return ContactLogService(
        contact_repository=ContactRepository(engine=engine),
        log_repository=LogRepository(engine=engine),
    )


contact_log_service = new_contact_service()

# class LogNumbers:
#     def __init__(self, logs: List[MLog]):
#         self.__log_id_to_number = {}
#         self.__number_to_log_id = {}
#         for i in range(len(logs)):
#             log_id = logs[i].id
#             self.__log_id_to_number[log_id] = i
#             self.__number_to_log_id[i] = log_id
#
#     def get_log_id_by_number(self, number: int) -> int | None:
#         return self.__number_to_log_id.get(number)
#
#     def get_number_by_log_id(self, log_id: int) -> int | None:
#         return self.__log_id_to_number.get(log_id)
