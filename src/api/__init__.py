from fastapi import APIRouter
from src.api.contacts.router import router as contacts_router

router = APIRouter()
router.include_router(contacts_router)
