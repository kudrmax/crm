from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.keyboards import contact_profile_kb, main_kb
from src.bot.states import DeleteContactState, ContactProfileState
from src.errors import ContactNotFoundError

router = Router()


@router.message(DeleteContactState.waiting_confirmation, F.text.lower().contains('сancel'))
async def choose_action(message: Message, state: FSMContext):
    await message.answer("Canceled", reply_markup=contact_profile_kb())
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
            await Helper.delete_contact(name)
            await message.answer(f"Contact with name {name} was deleted.", reply_markup=main_kb())
            await state.clear()
        except ContactNotFoundError:
            await message.answer(f"Contact with name {name} not found.")
