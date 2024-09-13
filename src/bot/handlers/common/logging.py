from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message

from src.bot.contact_helper import ContactHelper
from src.bot.keyboards.keyboards import make_row_keyboard_by_list, make_log_menu_kb
from src.bot.states.states import AddLog

router = Router()


async def start_logging(
        message: Message,
        state: FSMContext,
        final_state: StatesGroup | None,
        final_reply_markup,
):
    await state.update_data(final_state=final_state)
    await state.update_data(reply_markup=final_reply_markup)
    await message.answer(
        'Type log or cancel:',
        reply_markup=make_row_keyboard_by_list(['Stop logging'])
    )
    await state.set_state(AddLog.logging)


@router.message(AddLog.logging, F.text == 'Stop logging')
async def stop_logging(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Stopped logging', reply_markup=data['final_reply_markup'])
    await state.set_state(data['final_state'])


@router.message(AddLog.logging)
async def add_log(message: Message, state: FSMContext):
    data = await state.get_data()
    new_log = message.text
    if await ContactHelper.add_log(log_str=new_log, name=data['name']):
        await message.reply('✅')
        return
    await message.reply('❌')