from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from src.bot.handlers.search_contact import search_contact
from src.bot.states.states import AddLog, FindContactState
from src.bot.keyboards.keyboards import make_row_keyboard_by_list

router = Router()


@router.message(StateFilter(None), F.text == 'Add log')
async def add_log(message: Message, state: FSMContext):
    await search_contact(
        message,
        state,
        next_state=AddLog.log_menu,
        cancel_state=None,
        reply_markup=ReplyKeyboardRemove(),
    )

# @router.message(StateFilter(None), F.text == 'Add log')
# async def add_log(message: Message, state: FSMContext):
#     await state.set_state(FindContactState.type_name)
#     await state.update_data(state_after_search=AddLog.log_menu)


# @router.message(StateFilter(None), F.text == 'Add log')
# async def add_log(message: Message, state: FSMContext):
#     await message.answer(
#         'Type name:',
#         reply_markup=make_row_keyboard_by_list(['Cancel'])
#     )
#     await state.set_state(AddLog.name)
#
#
# @router.message(AddLog.name)
# async def name(message: Message, state: FSMContext):
#     name = message.text
#     await message.answer(
#         'Type name:',
#         reply_markup=make_row_keyboard_by_list(['Cancel'])
#     )


# @router.message(AddLog.log_menu)
# async def name(message: Message, state: FSMContext):
#     await message.answer(
#         'Log menu',
#     )
