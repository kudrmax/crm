from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.contacts.dao import DAOContact
from src.api.contacts.schemas import SContactCreate, SContactUpdate

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.get("/")
async def get_all_contacts(
        dao: DAOContact = Depends()
):
    return await dao.get_all()


@router.get("/{contact_id}")
async def get_one_or_none_contacts(
        contact_id: UUID,
        dao: DAOContact = Depends()
):
    return await dao.get_one_or_none(contact_id)


@router.post("/")
async def add_contact(
        new_contact: SContactCreate,
        dao: DAOContact = Depends()
):
    return await dao.create(new_contact)


@router.delete("/{contact_id}")
async def delete_contact(
        contact_id: UUID,
        dao: DAOContact = Depends()
):
    return await dao.delete(contact_id)


@router.put("/{contact_id}")
async def update_contact(
        contact_id: UUID,
        update_contact: SContactUpdate,
        dao: DAOContact = Depends()
):
    return await dao.update(contact_id, update_contact)


