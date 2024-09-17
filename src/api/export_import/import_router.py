from fastapi import APIRouter, Depends

from src.api.export_import.dao import DAOExportImport

router = APIRouter(
    tags=["Import"],
)


@router.post("/import_from_csv/")
async def import_from_csv(
        dao: DAOExportImport = Depends()
):
    await dao.import_contacts_to_csv()
    await dao.import_logs_to_csv()


@router.post("/import_from_csv/contacts")
async def import_contacts_to_csv(
        dao: DAOExportImport = Depends()
):
    return await dao.import_contacts_to_csv()


@router.post("/import_from_csv/logs")
async def import_logs_to_csv(
        dao: DAOExportImport = Depends()
):
    return await dao.import_logs_to_csv()
