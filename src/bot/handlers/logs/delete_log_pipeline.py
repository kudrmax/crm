from typing import List

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.keyboards import make_row_keyboard_by_list, edit_log_kb, contact_profile_kb
from src.bot.states import ContactProfileState, DeleteLogsState
from src.errors import UnprocessableEntityError, NotFoundError
from src.models.log.models import MLogWithNumbers
from src.services.contact_log.service import contact_log_service
from src.services.telegram.service import telegram_service

router = Router()


@router.message(ContactProfileState.choose_action, F.text.lower().contains('delete log'))
async def delete_logs_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    logs = contact_log_service.get_logs_by_contact_name(name, need_numbers=True)
    if len(logs) == 0:
        await message.answer(f'👎🏻 There is no logs for {name}')
        return
    await state.update_data(logs=logs)
    await message.answer(
        telegram_service.convert_logs_to_str(logs), # TODO превратить в один пайплайн get_logs
        # parse_mode=ParseMode.MARKDOWN_V2,
    )
    await message.answer(
        'Type number of log to delete:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(DeleteLogsState.typing_number)


@router.message(DeleteLogsState.typing_number, F.text.lower().contains('cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.update_data(logs=None)
    await message.answer(f'Canceled', reply_markup=contact_profile_kb())
    await state.set_state(ContactProfileState.choose_action)


@router.message(DeleteLogsState.typing_number)
async def choose_number(message: Message, state: FSMContext):
    number = message.text
    data = await state.get_data()
    logs: List[MLogWithNumbers] = data['logs']

    deleted_log = None
    for log in logs:
        if log.telegram_number == int(number): # TODO добавить проверку на то, что это конвертируется в int
            deleted_log = log
            break

    if not deleted_log:
        await message.answer(f'There is no log with number {int(number)}. Type another number:')
        return

    log_id = deleted_log.id
    try:
        contact_log_service.delete_log_by_log_id(log_id)
        # await Helper.delete_log(log_id)
    except NotFoundError as e:
        await message.answer(f'There is no log with number {int(number)}. Type another number:')
    else:
        await message.answer(
            f'Log was deleted successfully.',
            reply_markup=contact_profile_kb()
        )
        await state.update_data(logs=None)
        await state.update_data(log_id=None)
        await state.set_state(ContactProfileState.choose_action)