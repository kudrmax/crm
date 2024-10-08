from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.keyboards import make_row_keyboard_by_list, edit_log_kb, contact_profile_kb
from src.bot.states import EditLogsState, ContactProfileState
from src.errors import UnprocessableEntityError

router = Router()


@router.message(ContactProfileState.choose_action, F.text.lower().contains('edit log'))
async def edit_logs_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    log_str, numbers_to_log_id = await Helper.get_all_logs(data['name'])
    if Helper.text_is_empty(log_str):
        await message.answer(f'👎🏻 There is no logs for {name}')
        return
    await state.update_data(numbers_to_log_id=numbers_to_log_id)
    await message.answer(Helper.create_str_for_logs(log_str, name), parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer(
        'Type number of log to edit:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(EditLogsState.typing_number)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.update_data(numbers_to_log_id=None)
    await message.answer(f'Canceled', reply_markup=contact_profile_kb())
    await state.set_state(ContactProfileState.choose_action)


@router.message(EditLogsState.typing_number, F.text.lower().contains('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.update_data(numbers_to_log_id=None)
    await message.answer(f'Canceled', reply_markup=contact_profile_kb())
    await state.set_state(ContactProfileState.choose_action)


@router.message(EditLogsState.typing_number)
async def choose_number(message: Message, state: FSMContext):
    number = message.text
    data = await state.get_data()
    numbers_to_log_id = data['numbers_to_log_id']
    if number not in numbers_to_log_id:
        await message.answer(f'There is no log with number {int(number)}. Type another number:')
        return
    log_id = numbers_to_log_id[number]
    await state.update_data(log_id=log_id)
    await message.answer(
        f'You are going to update log with log_id={log_id}',
        reply_markup=edit_log_kb()
    )
    await state.set_state(EditLogsState.choose_what_to_edit)


@router.message(EditLogsState.choose_what_to_edit, F.text.lower().contains('edit text'))
async def edit_text(message: Message, state: FSMContext):
    await message.answer(
        f'Type new text:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(EditLogsState.typing_new_text)


@router.message(EditLogsState.typing_new_text)
async def new_text(message: Message, state: FSMContext):
    new_text = message.text
    data = await state.get_data()
    log_id = data['log_id']
    await Helper.edit_log_text(log_id=log_id, new_text=new_text)
    await message.answer(
        f'Text was edited successfully.',
        reply_markup=contact_profile_kb()
    )
    await state.update_data(numbers_to_log_id=None)
    await state.update_data(log_id=None)
    await state.set_state(ContactProfileState.choose_action)


@router.message(EditLogsState.choose_what_to_edit, F.text.lower().contains('edit date'))
async def edit_date(message: Message, state: FSMContext):
    await message.answer(
        f'Type new date:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(EditLogsState.typing_new_date)


@router.message(EditLogsState.typing_new_date)
async def new_date(message: Message, state: FSMContext):
    new_date = message.text
    data = await state.get_data()
    log_id = data['log_id']
    try:
        await Helper.edit_log_date(log_id=log_id, new_date=new_date)
    except UnprocessableEntityError:
        await message.answer(f'A date should be in the format "YYYY-MM-DD". Type another date:')
    else:
        await message.answer(
            f'Date was edited successfully.',
            reply_markup=contact_profile_kb()
        )
        await state.update_data(numbers_to_log_id=None)
        await state.update_data(log_id=None)
        await state.set_state(ContactProfileState.choose_action)
