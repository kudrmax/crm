import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from src.bot.handlers.pipelines.contact_profile_get import start_get_profile_pipeline
from src.bot.handlers.pipelines.logs_logging import create_log
from src.bot.keyboards import finish_kb
from src.bot.states import Voice2TextState
from src.services.contact_log.service import contact_log_service
from src.services.gpt.service import gpt_service
from src.services.voice2text.service import voice2text_service

VOICE_DIR = "files/voice_messages"
os.makedirs(VOICE_DIR, exist_ok=True)

router = Router()


async def start_gpt_pipeline(message: Message, state: FSMContext):
    await message.answer('Send a voice message', reply_markup=finish_kb())
    await state.set_state(Voice2TextState.waiting_for_voice)


@router.message(Voice2TextState.waiting_for_voice, F.text.lower().contains('finish'))
async def finish(message: Message, state: FSMContext):
    await start_get_profile_pipeline(message, state)


@router.message(Voice2TextState.waiting_for_voice, F.voice)
async def voice(message: Message, state: FSMContext):
    voice = message.voice
    file_id = voice.file_id

    await message.answer(f"Processing voice message with duration {voice.duration} sec...")

    file_name = f"{file_id}.ogg"
    file_path = os.path.join(VOICE_DIR, file_name)
    file = await message.bot.get_file(file_id)
    await message.bot.download_file(file.file_path, file_path)

    text = voice2text_service.voice2text(file_path)
    await message.reply(text)
    # TODO удалять файл после

    bullet_text, _ = gpt_service._get_bullet_list_from_text(text)
    await message.reply(bullet_text)

    data = await state.get_data()
    contact_id = contact_log_service.get_contact_id_by_name(data['name'])
    date = data['date'] if 'date' in data else None

    await create_log(message, state, contact_id, bullet_text, date)
