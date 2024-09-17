from typing import List

from fastapi import APIRouter, Depends

from src.api.contacts.dao import DAOContact
from src.api.contacts.schemas import SContactCreate, SContactUpdate, SContactRead

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.get("/")
async def get_all_contacts(
        dao: DAOContact = Depends()
):
    return await dao.get_all()


@router.get("/get_last_contacts")
async def get_last_contacts(
        contact_count: int = 5,
        dao: DAOContact = Depends()
) -> List[SContactRead]:
    return await dao.get_last_contacts(contact_count)


@router.post("/new", response_model=SContactRead)
async def add_contact(
        new_contact: SContactCreate,
        dao: DAOContact = Depends()
) -> SContactRead:
    return await dao.create(new_contact)


@router.get("/{name}")
async def get_contact_by_name(
        name: str,
        dao: DAOContact = Depends()
) -> SContactRead | None:
    return await dao.get_contact(name)


@router.delete("/{name}")
async def delete_contact(
        name: str,
        dao: DAOContact = Depends()
) -> SContactRead | None:
    return await dao.delete(name)


@router.put("/{name}")
async def update_contact(
        name: str,
        update_contact: SContactUpdate,
        dao: DAOContact = Depends()
) -> SContactRead:
    return await dao.update(name, update_contact)


@router.get("/{name}/search")
async def search_contact(
        name: str,
        name_count: int = 6,
        dao: DAOContact = Depends()
) -> List[SContactRead]:
    return await dao.search(name, name_count)
