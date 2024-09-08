from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.contacts.keyboards import make_edit_contact_kb
from src.bot.handlers.contacts.states import ProcessContactState, EditContactState
from src.bot.handlers.main_menu import make_main_menu

router = Router()


@router.message(ProcessContactState.choose_action)
async def choose_action(message: Message, state: FSMContext):
    button_text = message.text
    match button_text:
        case 'Get log ❌':
            pass
        case 'Add log ❌':
            pass
        case 'Edit contact':
            await message.answer(
                'Choose what to edit:',
                reply_markup=make_edit_contact_kb()
            )
            await state.set_state(EditContactState.choose_what_edit)
        case 'Delete contact ❌':
            pass
        case 'Exit':
            await state.clear()
            await message.answer(
                'Choose option:',
                reply_markup=make_main_menu()
            )
        case _:
            pass
