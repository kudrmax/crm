from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import make_row_keyboard_by_list, contact_profile_kb
from src.bot.states import AddContactState, ContactProfileState
from src.errors import ContactAlreadyExistsErr
from src.models.contact.model import MContactCreate
from src.models.log.models import MLogCreate
from src.services.contact_log.service import contact_log_service
from src.services.telegram.service import telegram_service

router = Router()


async def start_create_contact_pipeline(message: Message, state: FSMContext):
    await message.answer(
        'Type name of new contact:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(AddContactState.name)


@router.message(AddContactState.name, F.text.lower().contains('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        telegram_service.main_menu.get_post(),
        reply_markup=telegram_service.main_menu.get_kb(),
        # TODO сделать так, чтобы после создания контакта ты переходил в его профиль
    )


@router.message(AddContactState.name)
async def set_name(message: Message, state: FSMContext):
    name: str = message.text

    try:
        contact_log_service.create_contact(MContactCreate(name=name))
        await message.reply(
            f'✅ Contact *{name}* was added',  # TODO добавить жирный текст
            reply_markup=contact_profile_kb(),
        )

        # заполняем пустой лог, чтобы контакт сразу же появился в поиске
        contact_id = contact_log_service.get_contact_id_by_name(name)
        contact_log_service.create_log(MLogCreate(
            contact_id=contact_id,
            text=""
        ))

        await state.clear()
        await state.update_data(name=name)
        await state.set_state(ContactProfileState.choose_action)
    except ContactAlreadyExistsErr:
        await message.reply(
            f'❌ Contact *{name}* already exists. Type another name or cancel:'
        )  # TODO добавить жирный текст
