from typing import List

from src.models.contact.model import MContact, MContactCreate, MContactUpdate
from src.storage.postgres.repositories.contacts.errors import ContactNotFoundErr
from src.storage.postgres.repositories.contacts.repository import ContactRepository


class ContactService:
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    def get_all_contacts(self) -> List[MContact]:
        return self.repository.get_all()

    def get_contact_by_name(self, name: str) -> MContact | None:
        return self.repository.get_by_name(name)

    def create_contact(self, contact: MContactCreate) -> bool:
        try:
            return self.repository.create(contact)
        except ContactNotFoundErr:
            raise ContactNotFoundErr()

    def update_contact_by_name(self, name: str, new_contact: MContactUpdate) -> bool:
        return self.repository.update_by_name(name, new_contact)

    def delete_contact_by_name(self, name: str) -> bool:
        return self.repository.delete_by_name(name)
