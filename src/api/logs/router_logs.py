# from uuid import UUID
#
# from fastapi import APIRouter, Depends
#
# from src.api.contacts.dao import DAOContact
# from src.api.contacts.schemas import SContactCreate, SContactUpdate
# from src.api.logs.dao import DAOLog
# from src.api.logs.schemas import SLogData
#
# router = APIRouter(
#     prefix="/contacts/logs",
#     tags=["Logs"],
# )
#
#
# @router.get("/{contact_id}")
# async def get_log_by_id(
#         contact_id: UUID,
#         dao: DAOLog = Depends()
# ):
#     return await dao.get_log(contact_id)
#
#
# @router.put("/{contact_id}")
# async def add_data_to_log_by_id(
#         contact_id: UUID,
#         log_data: SLogData,
#         dao: DAOLog = Depends()
# ):
#     return await dao.add_data_to_log(contact_id, log_data)
#
#
# @router.delete("/{contact_id}")
# async def delete_log_by_id(
#         contact_id: UUID,
#         dao: DAOLog = Depends()
# ):
#     return await dao.remove_log(contact_id)
