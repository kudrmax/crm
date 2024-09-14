from aiogram.fsm.state import StatesGroup, State


class ContactProfileState(StatesGroup):
    choose_action = State()


class FindContactState(StatesGroup):
    typing_name = State()
    choosing_name = State()


class EditContactState(StatesGroup):
    choose_what_edit = State()
    waiting_for_data = State()


class AddContactState(StatesGroup):
    name = State()


class AddLog(StatesGroup):
    menu = State()
    logging = State()


class DeleteContactState(StatesGroup):
    waiting_confirmation = State()