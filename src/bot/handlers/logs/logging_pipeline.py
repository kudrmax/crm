import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message

from src.bot.handlers.contacts.search_contact_pipeline import search_contact_from_main_to_profile
from src.bot.helper import Helper
from src.bot.keyboards import make_row_keyboard_by_list, logging_kb
from src.bot.states import AddLog
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
        reply_markup=logging_kb()
    )
    await state.set_state(AddLog.logging)


@router.message(AddLog.logging, F.text.lower().contains('set date to yesterday'))
async def set_date_to_yesterday(message: Message, state: FSMContext):
    date = datetime.date.today() - datetime.timedelta(days=1)
    await state.update_data(date=date)
    await message.answer('Date was set to yesterday')


@router.message(AddLog.logging, F.text.lower().contains('set date to today'))
async def set_date_to_today(message: Message, state: FSMContext):
    await state.update_data(date=None)
    await message.answer('Date was set to today')


@router.message(AddLog.logging, F.text.lower().contains('find contact'))
async def find_contact(message: Message, state: FSMContext):
    await state.clear()
    await search_contact_from_main_to_profile(message, state)


@router.message(AddLog.logging, F.text.lower().contains('stop logging'))
async def stop_logging(message: Message, state: FSMContext):
    await state.update_data(logs_are_got=False)
    data = await state.get_data()
    await state.update_data(date=None)
    await message.answer('Stopped logging', reply_markup=data['final_reply_markup'])
    await state.set_state(data['final_state'])


@router.message(AddLog.logging)
async def add_log(message: Message, state: FSMContext):
    data = await state.get_data()
    new_log = message.text
    try:
        date = data['date'] if 'date' in data else None
        await Helper.add_log(log_str=new_log, name=data['name'], date=date)
        reply_text = '✅' if not date else f'✅ on {date}'
        await message.reply(reply_text)
    except ContactNotFoundError:
        await message.reply('❌')
        await message.answer(f"Contact with name {data['name']} not found. Aborted.")
        raise
