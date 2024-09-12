from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.contact_helper import ContactHelper
from src.bot.keyboards.keyboards import make_row_keyboard_by_list, make_log_menu_kb
from src.bot.states.states import AddLog

router = Router()


@router.message(AddLog.menu, F.text == 'Start logging')
async def get_logs(message: Message, state: FSMContext):
    await message.answer(
        'Type log or cancel:',
        reply_markup=make_row_keyboard_by_list(['Stop logging'])
    )
    await state.set_state(AddLog.logging)


@router.message(AddLog.logging, F.text == 'Stop logging')
async def get_logs(message: Message, state: FSMContext):
    await state.set_state(AddLog.menu)
    await message.answer('Stopped logging', reply_markup=make_log_menu_kb())


@router.message(AddLog.logging)
async def get_logs(message: Message, state: FSMContext):
    data = await state.get_data()
    new_log = message.text
    if await ContactHelper.add_log(log_str=new_log, name=data['name']):
        await message.reply('✅')
        return
    await message.reply('❌')
