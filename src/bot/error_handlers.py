from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent
from requests.exceptions import ConnectionError

from src.bot.keyboards import main_kb
from src.errors import UnknownError, UnprocessableEntityError

router = Router()


async def go_to_main_menu_after_error(event: ErrorEvent, state: FSMContext):
    if event.update.message:
        # @todo перенести event.exception в логирование
        await event.update.message.answer(
            f"Oops, something went wrong!\n\nError:\n{event.exception}",
            reply_markup=main_kb()
        )
    await state.clear()


@router.errors(ExceptionTypeFilter(ConnectionError))
async def connection_error(event: ErrorEvent, state: FSMContext):
    await event.update.message.answer(f"Can't connect to server.")
    await go_to_main_menu_after_error(event, state)


@router.errors(ExceptionTypeFilter(UnknownError))
async def unknown_error(event: ErrorEvent, state: FSMContext):
    await event.update.message.answer(f"Unknown Error")
    await go_to_main_menu_after_error(event, state)


@router.errors(ExceptionTypeFilter(UnprocessableEntityError))
async def connection_error(event: ErrorEvent, state: FSMContext):
    await event.update.message.answer(f"UnprocessableEntityError")
    await go_to_main_menu_after_error(event, state)


@router.errors()
async def all_errors(event: ErrorEvent, state: FSMContext):
    await go_to_main_menu_after_error(event, state)
