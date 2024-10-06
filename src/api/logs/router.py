import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.logs.dao import DAOLog
from src.api.contacts.models import MContact
from src.api.contacts.schemas import SContactCreate, SContactUpdate, SContactRead
from src.api.logs.schemas import SLogCreate, SLogRead, SEmptyLogCreate, SLogUpdate

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


@router.post("/new/empty")
async def add_empty_log(
        empty_log: SEmptyLogCreate,
        dao: DAOLog = Depends()
) -> SLogRead:
    return await dao.create_empty_log(empty_log)


@router.post("/new/yesterday")
async def add_log_at_yesterday(
        log: SLogCreate,
        dao: DAOLog = Depends()
) -> SLogRead:
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return await dao.create(log, date=yesterday)


@router.post("/new/{date}")
async def add_log_at_date(
        log: SLogCreate,
        date: datetime.date,
        dao: DAOLog = Depends()
) -> SLogRead:
    return await dao.create(log, date=date)


@router.get("/last_logs")
async def get_last_logs(
        days_count: int = 5,
        dao: DAOLog = Depends()
):
    return await dao.get_last_logs(days_count)


@router.get("/{name}")
async def get_all_logs(
        name: str,
        dao: DAOLog = Depends()
) -> List[SLogRead]:
    return await dao.get_all_logs_by_name(name)


@router.get("/{name}/by_date")
async def get_all_logs_grouped_by_date(
        name: str,
        dao: DAOLog = Depends()
):
    return await dao.get_all_logs_grouped_by_date(name)


@router.put("/edit/{log_id}/")
async def edit_log_by_id(
        log_id: int,
        log_update: SLogUpdate,
        dao: DAOLog = Depends()
) -> SLogRead:
    return await dao.edit_log_by_id(log_id, log_update)


@router.put("/edit/{log_id}/by_date")
async def edit_log_date_by_id(
        log_id: int,
        date_obj: datetime.date,
        dao: DAOLog = Depends()
):
    return await dao.edit_log_date_by_id(log_id, date_obj)


@router.delete("/{log_id}")
async def delete_log(
        log_id: int,
        dao: DAOLog = Depends()
) -> SLogRead | None:
    return await dao.delete(log_id)
