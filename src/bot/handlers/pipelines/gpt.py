import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from src.bot.handlers.pipelines.contact_profile_get import start_get_profile_pipeline
from src.bot.keyboards import finish_kb
from src.bot.states import Voice2TextState
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
    await message.answer(
        f"You send voice with duration {voice.duration} sec. File id is {voice.file_id}. Processing...")

    file_id = voice.file_id
    file_name = f"{file_id}.ogg"

    file_path = os.path.join(VOICE_DIR, file_name)

    file = await message.bot.get_file(file_id)
    await message.bot.download_file(file.file_path, file_path)

    text = voice2text_service.voice2text(file_path)
    await message.reply(text)

    # TODO удалять файл после


