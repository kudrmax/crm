import datetime

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


async def cancel_func(message: Message, state: FSMContext):
    await state.update_data(numbers_to_log_id=None)
    await state.update_data(log_id=None)
    await state.update_data(old_log_date=None)
    await state.update_data(old_log_text=None)
    await message.answer(f'Canceled', reply_markup=contact_profile_kb())
    await state.set_state(ContactProfileState.choose_action)


@router.message(ContactProfileState.choose_action, F.text.lower().contains('cancel'))
async def cancel1(message: Message, state: FSMContext):
    await cancel_func(message, state)


@router.message(EditLogsState.typing_number, F.text.lower().contains('cancel'))
async def cancel2(message: Message, state: FSMContext):
    await cancel_func(message, state)


@router.message(EditLogsState.choose_what_to_edit, F.text.lower().contains('cancel'))
async def cancel3(message: Message, state: FSMContext):
    await cancel_func(message, state)


@router.message(EditLogsState.typing_new_text, F.text.lower().contains('cancel'))
async def cancel4(message: Message, state: FSMContext):
    await cancel_func(message, state)


@router.message(EditLogsState.typing_new_date, F.text.lower().contains('cancel'))
async def cancel5(message: Message, state: FSMContext):
    await cancel_func(message, state)


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
    log = await Helper.get_log_by_id(log_id)
    log_text = log['log']
    log_datetime = log['datetime']
    dt = datetime.datetime.fromisoformat(log_datetime)
    log_date = dt.strftime("%Y-%m-%d")
    await state.update_data(old_log_text=log_text)
    await state.update_data(old_log_date=log_date)
    await message.answer(
        f"Log to edit:\n\n— Text: `{Helper._escape_markdown_v2(log_text)}`\n— Date: `{Helper._escape_markdown_v2(log_date)}`",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await message.answer(
        f'Choose option:',
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
    data =await state.get_data()
    await Helper.edit_log_text(log_id=log_id, new_text=new_text)
    await message.answer(
        "\n".join([
            f"Text was edited successfully.",
            f"",
            f"Old text: {data['old_log_text']}",
            f"New text: {new_text}",
        ]),
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
        "\n".join([
            f"Date was edited successfully.",
            f"",
            f"Old date: {data['old_log_date']}",
            f"New date: {new_date}",

        ]),
            reply_markup=contact_profile_kb()
        )
        await state.update_data(numbers_to_log_id=None)
        await state.update_data(log_id=None)
        await state.update_data(old_log_date=None)
        await state.update_data(old_log_text=None)
        await state.set_state(ContactProfileState.choose_action)
