from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.menu_main import start_main_menu_pipeline
from src.bot.handlers.pipelines.menu_contact import start_menu_contact_pipeline
from src.bot.keyboards import cancel_kb
from src.bot.states import DeleteContactState
from src.services.contact_log.service import contact_log_service

router = Router()


async def start_delete_contact_pipeline(message: Message, state: FSMContext):
    await state.update_data(logs_are_got=False)

    data = await state.get_data()
    name = data.get('name')

    await message.answer(
        f'Type "I want to delete contact X", where X is name of contact to delete {name}.',
        reply_markup=cancel_kb()
    )
    await state.set_state(DeleteContactState.waiting_confirmation)


@router.message(DeleteContactState.waiting_confirmation, F.text.lower().contains('cancel'))
async def choose_action(message: Message, state: FSMContext):
    await start_menu_contact_pipeline(message, state, text='Canceled')  # TODO переписать все cancel на что-то подобное


@router.message(DeleteContactState.waiting_confirmation)
async def delete(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']

    confirm_text = f'I want to delete contact {name}'
    if message.text != confirm_text:
        await message.answer(f'You text is not right. Try again or cancel')
        return

    contact_log_service.delete_contact_by_name(name)

    await start_main_menu_pipeline(message, state, text=f"Contact with name {name} was deleted.")
