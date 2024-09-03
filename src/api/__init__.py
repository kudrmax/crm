from fastapi import APIRouter
from src.api.contacts.router_contacts import router as contacts_router
from src.api.contacts.router_logs import router as logs_router

router = APIRouter()
router.include_router(contacts_router)
router.include_router(logs_router)
