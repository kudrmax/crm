from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message

from src.bot.helper.contact_helper import ContactHelper
from src.bot.keyboards.keyboards import make_row_keyboard_by_list
from src.bot.states.states import AddLog
from src.errors import ContactNotFoundError

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
    try:
        await ContactHelper.add_log(log_str=new_log, name=data['name'])
        await message.reply('✅')
    except ContactNotFoundError:
        await message.reply('❌')
        await message.answer(f"Contact with name {data['name']} not found. Aborted.")
        raise
