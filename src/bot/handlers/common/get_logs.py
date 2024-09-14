from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper.contact_helper import ContactHelper
from src.errors.errors import ContactNotFoundError


async def get_logs(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    try:
        all_logs = await ContactHelper.get_all_logs(name)
        if not all_logs or all_logs == "":
            await message.answer(f'There is no logs for {name}')
            return
        await message.answer(f'Logs for {name}')
        await message.answer(all_logs)
    except ContactNotFoundError:
        await message.answer(f"Contact with name {name} not found.")
