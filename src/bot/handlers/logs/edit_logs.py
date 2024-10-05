from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import ContactHelper
from src.bot.keyboards import make_row_keyboard_by_list, make_edit_log_menu_kb
from src.bot.states import EditLogsState, ContactProfileState

router = Router()


@router.message(ContactProfileState.choose_action, F.text == 'Edit logs')
async def edit_logs_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    log_str, numbers_to_log_id = await ContactHelper.get_all_logs_with_numbers(data['name'])
    await state.update_data(numbers_to_log_id=numbers_to_log_id)
    await message.answer(f'Logs:\n\n{log_str}')
    await message.answer(
        'Type number of log to edit:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(EditLogsState.typing_number)


@router.message(EditLogsState.typing_number)
async def choose_number(message: Message, state: FSMContext):
    number = message.text
    data = await state.get_data()
    numbers_to_log_id = data['numbers_to_log_id']
    if number not in numbers_to_log_id:
        await message.answer(f'There is no log with number {int(number)}. Type another number:')
        return
    log_id = numbers_to_log_id[number]
    await message.answer(
        f'You are going to update log with log_id={log_id}',
        reply_markup=make_edit_log_menu_kb()
    )
    await state.set_state(EditLogsState.menu)


@router.message(EditLogsState.menu, F.text == 'Edit text')
async def edit_text(message: Message, state: FSMContext):
    await message.answer(
        f'Type new text:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(EditLogsState.typing_new_text)


@router.message(EditLogsState.typing_new_text)
async def new_text(message: Message, state: FSMContext):
    new_text = message.text
    await message.reply(
        f'Type new text:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(EditLogsState.typing_new_text)


@router.message(EditLogsState.menu, F.text == 'Edit date')
async def edit_text(message: Message, state: FSMContext):
    pass
