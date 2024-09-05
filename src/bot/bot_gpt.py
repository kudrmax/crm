import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from decouple import config

from src.bot.handlers.main import make_main_menu
from src.bot.keyboards.simple_row_by_list import make_row_keyboard_by_list

main_router = Router()


class AddUserState(StatesGroup):
    waiting_for_name = State()
    waiting_for_edit_or_finish = State()


def make_user_options_menu():
    return make_row_keyboard_by_list([
        'Редактировать имя',
        'Завершить',
    ])


@main_router.message(StateFilter(None), Command("start"))
async def start_command(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=make_main_menu())


@main_router.message(lambda message: message.text == 'Добавить пользователя')
async def add_user(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя:")
    await state.set_state(AddUserState.waiting_for_name)


@main_router.message(AddUserState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    # Сохраняем имя пользователя и устанавливаем его как старое имя
    previous_data = await state.get_data()
    old_name = previous_data.get('user_name')

    # Обновляем данные с новым именем
    await state.update_data(user_name=user_name)

    if old_name:
        # Если старое имя существует, сообщаем о изменении
        await message.answer(f"Вы изменили имя с {old_name} на {user_name}")
    else:
        await message.answer(f"Имя пользователя установлено: {user_name}")

    await message.answer("Выберите действие:", reply_markup=make_user_options_menu())
    await state.set_state(AddUserState.waiting_for_edit_or_finish)


@main_router.message(AddUserState.waiting_for_edit_or_finish)
async def process_user_option(message: types.Message, state: FSMContext):
    user_option = message.text
    user_data = await state.get_data()
    user_name = user_data.get('user_name')

    if user_option == 'Редактировать имя':
        await message.answer("Введите новое имя пользователя:")
        await state.set_state(AddUserState.waiting_for_name)
    elif user_option == 'Завершить':
        await message.answer(f"Вы добавили пользователя по имени {user_name}")
        await message.answer("Выберите действие:", reply_markup=make_main_menu())
        await state.clear()


TOKEN = config("BOT_TOKEN")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
