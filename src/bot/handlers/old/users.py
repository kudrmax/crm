# from aiogram import Router, F
# from aiogram.filters import Command, StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.types import Message, ReplyKeyboardRemove
#
# from src.bot.keyboards.simple_row_by_list import get_row_keyboard_by_list
# from src.bot.keyboards.users import (
#     get_new_data_or_change_name_kb,
# )
#
# router = Router()
#
#
# class NewProfileState(StatesGroup):
#     typing_name = State()
#     choosing_update_or_not = State()
#     choosing_what_to_update = State()
#     typing_new_data = State()
#
#
# @router.message(StateFilter(None), Command('new_user'))
# async def cmd_new_user(message: Message, state: FSMContext):
#     await message.answer(
#         'Введите имя:',
#     )
#     await state.set_state(NewProfileState.choosing_update_or_not)
#
#
# @router.message(NewProfileState.choosing_update_or_not)
# async def name_done(message: Message, state: FSMContext):
#     await state.update_data(chosen_food=message.text.lower())
#     await message.answer(
#         text="Имя сохранено. Выберите действие:",
#         reply_markup=get_row_keyboard_by_list(['Изменить имя', 'Добавить данные', 'Завершить'])
#     )
#     await state.set_state(NewProfileState.choosing_what_to_update)
#
#
# @router.message(NewProfileState.choosing_what_to_update)
# async def what_to_update(message: Message, state: FSMContext):
#     print(NewProfileState.choosing_what_to_update)
#     print(NewProfileState.choosing_what_to_update.state)
#     await state.update_data(chosen_food=message.text.lower())
#     await message.answer(
#         text="Выберите действие:",
#         reply_markup=get_row_keyboard_by_list(['Добавить телефон', 'Добавить телеграм'])
#     )
#     await state.set_state(NewProfileState.typing_new_data)
#
#
# @router.message(NewProfileState.typing_new_data)
# async def typing_new_data(message: Message, state: FSMContext):
#     await state.update_data(chosen_food=message.text.lower())
#     await message.answer(
#         text="Выберите данные:",
#     )
#     await state.set_state(NewProfileState.choosing_update_or_not)
