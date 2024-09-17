from fastapi import APIRouter, Depends

from src.api.export_import.dao import DAOExportImport

router = APIRouter(
    tags=["Export"],
)


@router.post("/export_to_csv/")
async def export_to_csv(
        dao: DAOExportImport = Depends()
):
    await dao.export_contacts_to_csv()
    await dao.export_logs_to_csv()


@router.post("/export_to_csv/contacts")
async def export_contacts_to_csv(
        dao: DAOExportImport = Depends()
):
    return await dao.export_contacts_to_csv()


@router.post("/export_to_csv/logs")
async def export_contacts_to_csv(
        dao: DAOExportImport = Depends()
):
    return await dao.export_logs_to_csv()
