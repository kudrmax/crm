from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ErrorEvent, Update

from src.bot.handlers.menu_main import make_main_menu_kb
from src.errors.errors import *

from requests.exceptions import ConnectionError

router = Router()


async def go_to_main_menu_after_error(event: ErrorEvent, state: FSMContext):
    if event.update.message:
        await event.update.message.answer(
            f"Oops, something went wrong!\n\n{event.exception}",  # @todo перенести event.exception в логирование
            reply_markup=make_main_menu_kb()
        )
    await state.clear()


@router.errors(ExceptionTypeFilter(ConnectionError))
async def connection_error(event: ErrorEvent, state: FSMContext):
    await event.update.message.answer(f"Can't connect to server.")
    await go_to_main_menu_after_error(event, state)


@router.errors()
async def all_errors(event: ErrorEvent, state: FSMContext):
    await go_to_main_menu_after_error(event, state)

# @router.errors(ContactAlreadyExistsError)
# async def handle_contact_exists_error(event: ErrorEvent, state: FSMContext):
#     data = await state.get_data()
#     await event.update.message.answer(f"Contact {data['name']} already exists. Type another name:")
