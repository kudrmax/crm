import datetime
from typing import List

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.keyboards import make_row_keyboard_by_list, edit_log_kb, contact_profile_kb
from src.bot.states import EditLogsState, ContactProfileState
from src.errors import UnprocessableEntityError
from src.models.log.models import MLogWithNumbers, MLogUpdate
from src.services.contact_log.service import contact_log_service
from src.services.telegram.service import telegram_service

router = Router()


@router.message(ContactProfileState.choose_action, F.text.lower().contains('edit log'))
async def edit_logs_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    logs = contact_log_service.get_logs_by_contact_name(data['name'], need_numbers=True)
    logs_str = telegram_service.get_logs_post(logs)
    # log_str, numbers_to_log_id = await Helper.get_all_logs(data['name'])
    if len(logs) == 0:
        await message.answer(f'👎🏻 There is no logs for {name}')
        return

    await state.update_data(logs=logs)
    await message.answer(
        logs_str,
        # parse_mode=ParseMode.MARKDOWN_V2,
    )
    await message.answer(
        'Type number of log to edit:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(EditLogsState.typing_number)


async def cancel_func(message: Message, state: FSMContext):
    await state.update_data(logs=None)
    await state.update_data(edited_log=None)
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
    logs: List[MLogWithNumbers] = data['logs']

    edited_log = None
    for log in logs:
        if log.telegram_number == int(number): # TODO добавить проверку что если пользователь введет букву
            edited_log = log

    if edited_log is None:
        await message.answer(f'There is no log with number {int(number)}. Type another number:')
        return

    await state.update_data(edited_log=edited_log)
    # log = await Helper.get_log_by_id(log_id)
    log_text = edited_log.text
    log_datetime = edited_log.datetime
    log_date = log_datetime.strftime("%Y-%m-%d")

    # dt = datetime.datetime.fromisoformat(log_datetime)
    # log_date = dt.strftime("%Y-%m-%d")
    await state.update_data(old_log_text=log_text)
    await state.update_data(old_log_date=log_date)
    await message.answer(
        f"Log to edit:\n\n— Text: `{log_text}`\n— Date: `{log_date}`",
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
    data = await state.get_data()
    edited_log: MLogWithNumbers = data['edited_log']

    new_text = message.text

    contact_log_service.update_log_by_log_id(edited_log.id, MLogUpdate(text=new_text))
    # await Helper.edit_log_text(log_id=log_id, new_text=new_text)
    await message.answer(
        "\n".join([
            f"Text was edited successfully.",
            f"",
            f"Old text: {data['old_log_text']}",
            f"",
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
    edited_log = data['edited_log']
    try:
        pass # TODO написать логику добавления лога в конец дня
        # await Helper.edit_log_date(log_id=log_id, new_date=new_date)
    except UnprocessableEntityError:
        await message.answer(f'A date should be in the format "YYYY-MM-DD". Type another date:')
    else:
        await message.answer(
        "\n".join([
            f"Date was edited successfully.",
            f"",
            f"Old date: {data['old_log_date']}",
            f"",
            f"New date: {new_date}",

        ]),
            reply_markup=contact_profile_kb()
        )
        await state.update_data(numbers_to_log_id=None)
        await state.update_data(log_id=None)
        await state.update_data(old_log_date=None)
        await state.update_data(old_log_text=None)
        await state.set_state(ContactProfileState.choose_action)
