from typing import List

from src.models.contact.model import MContact, MContactCreate, MContactUpdate
from src.models.log.models import MLogUpdate, MLog
from src.storage.postgres.connection.engine import engine
from src.errors import ContactNotFoundErr, ContactAlreadyExistsErr
from src.storage.postgres.repositories.contacts.repository import ContactRepository
from src.storage.postgres.repositories.logs.repository import LogRepository


class ContactLogService:
    def __init__(self, contact_repository: ContactRepository, log_repository: LogRepository):
        self.contact_repository = contact_repository
        self.log_repository = log_repository

    def get_all_contacts(self) -> List[MContact]:
        return self.contact_repository.get_all()

    def get_contact_by_name(self, name: str) -> MContact | None:
        return self.contact_repository.get_by_name(name)

    def get_last_contacts(self) -> List[MContact]:
        # TODO сделать так, чтобы получать последние созданные контакты, у которых пока 0 логов
        ids = self.log_repository.get_last_contact_ids()
        return self.contact_repository.get_by_contact_ids(ids)

    def get_log_by_log_id(self, log_id: int) -> MLog | None:
        return self.log_repository.get_by_id(log_id)

    def get_logs_by_contact_name(self, name: str) -> List[MLog]:
        contact = self.contact_repository.get_by_name(name)
        return self.log_repository.get_by_contact_id(contact.id)

    def create_contact(self, contact: MContactCreate) -> bool:
        try:
            return self.contact_repository.create(contact)
        except ContactAlreadyExistsErr:
            raise ContactAlreadyExistsErr()

    def update_contact_by_name(self, name: str, new_contact: MContactUpdate) -> bool:
        return self.contact_repository.update_by_name(name, new_contact)

    def delete_contact_by_name(self, name: str) -> bool:
        return self.contact_repository.delete_by_name(name)

    @staticmethod
    def get_names_from_models(contacts: List[MContact]) -> List[str]:
        return [contact.name for contact in contacts]


def new_contact_service() -> ContactLogService:
    return ContactLogService(
        contact_repository=ContactRepository(engine=engine),
        log_repository=LogRepository(engine=engine),
    )


contact_log_service = new_contact_service()
