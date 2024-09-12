from aiogram import Router

from .menu_contacts import router as contacts_router
from .add_contact import router as add_contact_router
from .btn_find_contact import router as find_contact_router
from .process_contact import router as process_contact_router
from .edit_contact import router as edit_contact_router
from .menu_logs import router as menu_logs_router
from .search_contact import router as search_contact_router

router = Router()

router.include_routers(
    contacts_router,
    add_contact_router,
    find_contact_router,
    process_contact_router,
    edit_contact_router,
    menu_logs_router,
    search_contact_router,
)
