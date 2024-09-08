from aiogram import Router

from .contacts import router as contacts_router
from .add_contact import router as add_contact_router
from .find_contact import router as find_contact_router
from .process_contact import router as process_contact_router
from .edit_contact import router as edit_contact_router

router = Router()

router.include_routers(
    contacts_router,
    add_contact_router,
    find_contact_router,
    process_contact_router,
    edit_contact_router,
)
