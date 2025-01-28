from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup

from src.bot.helper import Helper
from src.bot.keyboards import make_row_keyboard_by_list, make_keyboard_by_lists, main_kb, contact_profile_kb
from src.bot.states import FindContactState, ContactProfileState
from src.errors import ContactNotFoundError, NotFoundError
from src.services.contact_log.service import contact_log_service
from src.services.telegram.service import telegram_service

router = Router()


async def start_search_contact_pipeline(
        message: Message,
        state: FSMContext,
        final_state: StatesGroup | None,
        start_state: StatesGroup | None,
        final_reply_markup: ReplyKeyboardMarkup,
        start_reply_markup: ReplyKeyboardMarkup,
):
    await state.update_data(final_state=final_state)
    await state.update_data(start_state=start_state)
    await state.update_data(final_reply_markup=final_reply_markup)
    await state.update_data(start_reply_markup=start_reply_markup)

    last_contacts = contact_log_service.get_last_contacts()
    last_contacts_names = contact_log_service.get_names_from_models(
        last_contacts)  # TODO добавить рядом с именем общее количество логов
    await state.update_data(last_contacts_names=set(last_contacts_names))

    await message.answer(
        'Type name or select from list:',
        reply_markup=make_keyboard_by_lists(
            [[name] for name in last_contacts_names] + [['Cancel ⬅️']]
        )
    )

    await state.set_state(FindContactState.typing_name)


async def search_contact_from_main_to_profile(message: Message, state: FSMContext):
    # TODO удалить функцию. Каждый раз нужно начинать осознанно, через start_search_contact_pipeline (нврн)
    await start_search_contact_pipeline(
        message=message,
        state=state,
        start_state=None,
        start_reply_markup=main_kb(),
        final_state=ContactProfileState.choose_action,
        final_reply_markup=contact_profile_kb(),
    )


async def set_start_state(message: Message, state: FSMContext, text: str):
    data = await state.get_data()
    start_state = data.get('start_state')
    start_reply_markup = data.get('start_reply_markup')

    await message.answer(text, reply_markup=start_reply_markup)

    if start_state:
        await state.set_state(start_state)
        return

    await state.clear()


async def set_last_state(message: Message, state: FSMContext, name: str):
    await state.update_data(name=name)

    contact = contact_log_service.get_contact_by_name(name)
    logs = contact_log_service.get_logs_by_contact_name(name, need_numbers=True)
    logs_str = telegram_service.get_logs_post(logs)  # TODO перенести в отдельный один пайпдайн получения логов
    await message.answer(
        contact.to_string(),
        parse_mode=ParseMode.MARKDOWN_V2
    )

    data = await state.get_data()
    final_state = data.get('final_state')
    final_reply_markup = data.get('final_reply_markup')

    await message.answer(logs_str, reply_markup=final_reply_markup)
    await state.update_data(logs_are_got=True)

    await state.update_data(final_state=None)
    await state.update_data(start_state=None)
    await state.update_data(final_reply_markup=None)
    await state.update_data(start_reply_markup=None)
    await state.update_data(last_contacts_names=None)
    await state.update_data(similar_contacts_names=None)

    await state.set_state(final_state)


@router.message(FindContactState.typing_name, F.text.lower().contains('cancel'))
async def cancel(message: Message, state: FSMContext):
    await set_start_state(message, state, 'Canceled')


@router.message(FindContactState.typing_name)
async def contact(message: Message, state: FSMContext):
    data = await state.get_data()
    last_contacts_names = data['last_contacts_names'] if 'last_contacts_names' in data else set()

    name = message.text
    if name in last_contacts_names:
        await set_last_state(message, state, name)
        return

    await message.reply(f"🔎 Searching contact with name {name}")
    similar_contacts = contact_log_service.get_similar_contacts(name)
    if len(similar_contacts) == 0:
        await message.reply("🤷🏼‍♂️ No contacts found. Type another name or cancel.")
        return

    similar_contacts_names = [contact.name for contact in similar_contacts]
    await state.update_data(similar_contacts_names=set(similar_contacts_names))

    await message.answer(
        'Choose contact from list:',
        reply_markup=make_keyboard_by_lists(
            [[name] for name in similar_contacts_names] + [['Cancel ⬅️']]
        )
    )
    await state.set_state(FindContactState.choosing_name_from_list)


@router.message(FindContactState.choosing_name_from_list, F.text.lower().contains('cancel'))
async def cancel(message: Message, state: FSMContext):
    await set_start_state(message, state, 'Canceled')


@router.message(FindContactState.choosing_name_from_list)
async def contact(message: Message, state: FSMContext):
    data = await state.get_data()
    similar_contacts_names = data.get('similar_contacts_names')

    name = message.text
    if name in similar_contacts_names:
        await set_last_state(message, state, name)
        return

    await message.reply(
        'You should press a button, not type name. Choose contact from list or cancel:',
        # reply_markup=make_keyboard_by_lists(
        #     [[name] for name in similar_contacts_names] + [['Cancel ⬅️']]
        # )
    )
