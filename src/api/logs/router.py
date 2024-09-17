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


@router.post("/new")
async def add_log(
        log: SLogCreate,
        dao: DAOLog = Depends()
) -> SLogRead:
    return await dao.create(log)


@router.post("/empty_log")
async def add_empty_log(
        name: str,
        dao: DAOLog = Depends()
) -> SLogRead:
    return await dao.create_empty_log(name)


@router.get("/{name}")
async def get_all_logs(
        name: str,
        dao: DAOLog = Depends()
) -> List[SLogRead]:
    return await dao.get_all_by_name(name)
