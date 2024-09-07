from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.logs.dao import DAOLog
from src.api.contacts.models import MContact
from src.api.contacts.schemas import SContactCreate, SContactUpdate, SContactRead
from src.api.logs.schemas import SLogCreate, SLogRead

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)


@router.post("/")
async def add_log(
        log_create: SLogCreate,
        dao: DAOLog = Depends()
) -> SLogRead:
    return await dao.create(log_create)


@router.get("/{contact_id}")
async def get_all_logs(
        contact_id: UUID,
        dao: DAOLog = Depends()
) -> List[SLogRead]:
    return await dao.get_all_with_filter(contact_id=contact_id)

#
# @router.post("/by_date")
# async def get_log_by_date(
#         log_get_by_date: SLogGetByDate,
#         dao: DAOLog = Depends()
# ) -> List[SLogRead]:
#     return await dao.get_log_by_date(log_get_by_date)
