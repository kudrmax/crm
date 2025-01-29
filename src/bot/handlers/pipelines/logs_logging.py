import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message

from src.bot.handlers.pipelines.contact_serach import search_contact_from_main_to_profile
from src.bot.keyboards import logging_kb
from src.bot.states import AddLog
from src.errors import ContactNotFoundError
from src.models.log.models import MLogCreate
from src.services.contact_log.service import contact_log_service

router = Router()


async def start_logging(
        message: Message,
        state: FSMContext,
        final_state: StatesGroup | None,
        final_reply_markup,
):
    await state.update_data(final_state=final_state)
    await state.update_data(final_reply_markup=final_reply_markup)
    await message.answer(
        'Type log or cancel',
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
    await state.update_data(date=None)

    data = await state.get_data()
    await message.answer(
        'Stopped logging',
        reply_markup=data['final_reply_markup']
    )
    await state.set_state(data['final_state'])


@router.message(AddLog.logging)
async def add_log(message: Message, state: FSMContext):
    data = await state.get_data()

    log_text = message.text
    contact_id = contact_log_service.get_contact_id_by_name(data['name'])
    date = data['date'] if 'date' in data else None

    contact_log_service.create_log(MLogCreate(
        contact_id=contact_id,
        text=log_text,
        datetime=date,
    ))

    reply_text = '✅' if not date else f'✅ on {date}'
    await message.reply(reply_text)
