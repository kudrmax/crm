from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ErrorEvent, Update

from src.bot.handlers.menu_main import make_main_menu_kb
from src.errors.errors import *

router = Router()


@router.errors(ExceptionTypeFilter(InternalServerError))
async def handle_contact_exists_error(event: ErrorEvent, state: FSMContext):
    if event.update.message:
        await event.update.message.answer(
            "Oops, something went wrong!",
            reply_markup=make_main_menu_kb()
        )
    await state.clear()
    print(await state.get_data())

# @router.errors(ContactAlreadyExistsError)
# async def handle_contact_exists_error(event: ErrorEvent, state: FSMContext):
#     data = await state.get_data()
#     await event.update.message.answer(f"Contact {data['name']} already exists. Type another name:")
