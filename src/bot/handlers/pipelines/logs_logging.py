import datetime as dt

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message

from src.bot.handlers.pipelines.contact_serach import search_contact_from_main_to_profile
from src.bot.keyboards import logging_kb
from src.bot.states import AddLog
from src.models.log import MLogCreate
from src.services.contact_log.service import contact_log_service
from src.services.telegram.service import telegram_service

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


async def create_log(
        message: Message,
        state: FSMContext,
        contact_id: int,
        log_texts: str,
        date: dt.datetime | None = None
):
    log_text_list = log_texts.split('\n')
    log_text_list = [
        telegram_service.strip_log_text(l)
        for l in log_text_list if l != ''
    ]
    for log_text in log_text_list:
        contact_log_service.create_log(MLogCreate(
            contact_id=contact_id,
            text=log_text,
            datetime=date,
        ))

    if len(log_text_list) == 1:
        reply_text = f'✅' if not date else f'✅ on {date}'
    else:
        reply_text = f'✅x{len(log_text_list)}' if not date else f'✅x{len(log_text_list)} on {date}'
    await message.reply(reply_text)


@router.message(AddLog.logging, F.text.lower().contains('set date to yesterday'))
async def set_date_to_yesterday(message: Message, state: FSMContext):
    date = dt.date.today() - dt.timedelta(days=1)
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

    contact_id = contact_log_service.get_contact_id_by_name(data['name'])
    date = data['date'] if 'date' in data else None

    log_texts = message.text

    await create_log(message, state, contact_id, log_texts, date)
