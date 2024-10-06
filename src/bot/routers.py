from aiogram import Router

from src.bot.error_handlers import router as error_handlers

from src.bot.handlers.menu_main import router as menu_main

from src.bot.handlers.contacts.create_contact_pipline import router as create_contact_pipeline
from src.bot.handlers.contacts.delete_contact_pipeline import router as delete_contact_pipeline
from src.bot.handlers.contacts.edit_contact_pipeline import router as edit_contact_pipeline
from src.bot.handlers.contacts.menu_contact_profile import router as menu_contact_profile
from src.bot.handlers.contacts.search_contact_pipeline import router as search_contact_pipeline

from src.bot.handlers.logs.edit_logs_pipeline import router as edit_logs_pipeline
from src.bot.handlers.logs.logging_pipeline import router as logging_pipeline

router = Router()

router.include_routers(
    error_handlers,
    menu_main,
    create_contact_pipeline,
    delete_contact_pipeline,
    edit_contact_pipeline,
    menu_contact_profile,
    search_contact_pipeline,
    edit_logs_pipeline,
    logging_pipeline,
)
