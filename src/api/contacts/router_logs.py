from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.contacts.dao import DAOContact
from src.api.contacts.schemas import SContactCreate, SContactUpdate

router = APIRouter(
    prefix="/contacts/logs",
    tags=["Logs"],
)


@router.get("/{contact_id}")
async def get_log(
        contact_id: UUID,
        dao: DAOContact = Depends()
):
    return await dao.get_log(contact_id)

@router.put("/{contact_id}")
async def add_data_to_log(
        contact_id: UUID,
        log_data: str,
        dao: DAOContact = Depends()
):
    return await dao.add_data_to_log(contact_id, log_data)
