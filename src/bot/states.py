from aiogram.fsm.state import StatesGroup, State


class ContactProfileState(StatesGroup):
    choose_action = State()


class FindContactState(StatesGroup):
    typing_name = State()
    choosing_name_from_list = State()


class EditContactState(StatesGroup):
    choose_what_edit = State()
    waiting_for_data = State()


class EditLogsState(StatesGroup):
    typing_number = State()
    choose_what_to_edit = State()
    typing_new_text = State()
    typing_new_date = State()

class DeleteLogsState(StatesGroup):
    typing_number = State()


class AddContactState(StatesGroup):
    name = State()


class AddLog(StatesGroup):
    menu = State()
    logging = State()


class DeleteContactState(StatesGroup):
    waiting_confirmation = State()


class StatsState(StatesGroup):
    menu = State()
