from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.menu_main import make_main_menu_kb
from src.bot.helper import ContactHelper
from src.bot.keyboards import make_contact_profile_kb
from src.bot.states import DeleteContactState, ContactProfileState
from src.errors import ContactNotFoundError

router = Router()


@router.message(DeleteContactState.waiting_confirmation, F.text == 'Cancel')
async def choose_action(message: Message, state: FSMContext):
    await message.answer("Canceled", reply_markup=make_contact_profile_kb())
    await state.set_state(ContactProfileState.choose_action)


@router.message(DeleteContactState.waiting_confirmation)
async def delete(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    confirm_text = f'I want to delete contact {name}'
    if message.text != confirm_text:
        await message.answer(f'You text is not "{confirm_text}". Try again or cancel:')
        return
    else:
        try:
            await ContactHelper.delete(name)
            await message.answer(f"Contact with name {name} was deleted.", reply_markup=make_main_menu_kb())
            await state.clear()
        except ContactNotFoundError:
            await message.answer(f"Contact with name {name} not found.")
