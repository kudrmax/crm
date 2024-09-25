from aiogram import Router

from src.bot.handlers.contacts.menu_contacts import router as contacts_router
from src.bot.handlers.contacts.create_contact import router as add_contact_router
from src.bot.handlers.contacts.find_contact import router as find_contact_router
from src.bot.handlers.contacts.process_contact import router as process_contact_router
from src.bot.handlers.contacts.edit_contact import router as edit_contact_router
from src.bot.handlers.contacts.delete_contact import router as delete_router
from src.bot.handlers.logs.menu_logs import router as menu_logs_router
from src.bot.handlers.logs.get_logs import router as get_logs_router
from src.bot.handlers.logs.logging import router as logging_router
from src.bot.handlers.logs.edit_logs import router as edit_logs_router
from src.bot.handlers.common.search_contact import router as search_contact_router
from src.bot.handlers.common.logging import router as logging_common_router

router = Router()

router.include_routers(
    contacts_router,
    add_contact_router,
    find_contact_router,
    process_contact_router,
    edit_contact_router,
    menu_logs_router,
    search_contact_router,
    get_logs_router,
    logging_router,
    logging_common_router,
    delete_router,
    edit_logs_router,
)