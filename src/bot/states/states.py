from aiogram.fsm.state import StatesGroup, State


class ProcessContactState(StatesGroup):
    choose_action = State()


class FindContactState(StatesGroup):
    type_name = State()
    choose_name = State()


class EditContactState(StatesGroup):
    choose_what_edit = State()
    waiting_for_data = State()


class AddContactState(StatesGroup):
    name = State()


class AddLog(StatesGroup):
    menu = State()
    logging = State()

