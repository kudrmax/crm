from fastapi import APIRouter
from src.api.contacts.router import router as contacts_router
from src.api.logs.router import router as logs_router
from src.api.stats.router import router as stats_router
from src.api.export_import.export_router import router as export_router
from src.api.export_import.import_router import router as import_router

router = APIRouter(
    prefix='/api/v1'
)
router.include_router(contacts_router)
router.include_router(logs_router)
router.include_router(stats_router)
router.include_router(export_router)
router.include_router(import_router)
