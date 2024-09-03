from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.logs.dao import DAOLog
from src.api.logs.schemas import SLogCreate

router = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)


@router.get("/")
async def get_all_logs(
        dao: DAOLog = Depends()
):
    return await dao.get_all()


@router.get("/{log_id}")
async def get_one_or_none_logs(
        log_id: UUID,
        dao: DAOLog = Depends()
):
    return await dao.get_one_or_none(log_id)


@router.post("/")
async def add_log(
        new_log: SLogCreate,
        dao: DAOLog = Depends()
):
    return await dao.create(new_log)


# @router.delete("/{log_id}")
# async def delete_log(
#         log_id: UUID,
#         dao: DAOLog = Depends()
# ):
#     return await dao.delete(log_id)
#
#
# @router.put("/{log_id}")
# async def update_log(
#         log_id: UUID,
#         update_log: SContactUpdate,
#         dao: DAOLog = Depends()
# ):
#     return await dao.update(log_id, update_log)
