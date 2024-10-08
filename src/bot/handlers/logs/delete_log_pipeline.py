from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.helper import Helper
from src.bot.keyboards import make_row_keyboard_by_list, edit_log_kb, contact_profile_kb
from src.bot.states import ContactProfileState, DeleteLogsState
from src.errors import UnprocessableEntityError, NotFoundError

router = Router()


@router.message(ContactProfileState.choose_action, F.text == 'Delete log')
async def delete_logs_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    log_str, numbers_to_log_id = await Helper.get_all_logs(data['name'])
    await state.update_data(numbers_to_log_id=numbers_to_log_id)
    await message.answer(f'Logs:', parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer(log_str, parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer(
        'Type number of log to delete:',
        reply_markup=make_row_keyboard_by_list(['Cancel'])
    )
    await state.set_state(DeleteLogsState.typing_number)


@router.message(DeleteLogsState.typing_number, F.text == 'Cancel')
async def cancel(message: Message, state: FSMContext):
    await state.update_data(numbers_to_log_id=None)
    await message.answer(f'Canceled', reply_markup=contact_profile_kb())
    await state.set_state(ContactProfileState.choose_action)


@router.message(DeleteLogsState.typing_number)
async def choose_number(message: Message, state: FSMContext):
    number = message.text
    data = await state.get_data()
    numbers_to_log_id = data['numbers_to_log_id']
    if number not in numbers_to_log_id:
        await message.answer(f'There is no log with number {int(number)}. Type another number:')
        return
    log_id = numbers_to_log_id[number]
    try:
        await Helper.delete_log(log_id)
    except NotFoundError as e:
        await message.answer(f'There is no log with number {int(number)}. Type another number:')
    else:
        await message.answer(
            f'Log was deleted successfully.',
            reply_markup=contact_profile_kb()
        )
        await state.update_data(numbers_to_log_id=None)
        await state.update_data(log_id=None)
        await state.set_state(ContactProfileState.choose_action)

    # await state.update_data(log_id=log_id)
    # await message.answer(
    #     f'You are going to update log with log_id={log_id}',
    #     reply_markup=edit_log_kb()
    # )
    # await state.set_state(ContactProfileState.choose_what_to_edit)
