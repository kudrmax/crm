from aiogram import Router

from .contacts import router as contacts_router
from .add_contact import router as add_contact_router

router = Router()

router.include_routers(
    contacts_router,
    add_contact_router,
)