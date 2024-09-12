from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.contact_helper import ContactHelper
from src.bot.states.states import AddLog

router = Router()


@router.message(AddLog.menu, F.text == 'Get logs')
async def get_logs(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    all_logs = await ContactHelper.get_all_logs(name)
    if not all_logs or all_logs == "":
        await message.answer(f'There is no logs for {name}')
        return
    await message.answer(f'Logs for {name}')
    await message.answer(all_logs)
