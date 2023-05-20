from aiogram.dispatcher.filters.state import State, StatesGroup

class SignUpState(StatesGroup):
    name = State()
    tel = State()
    address_latitude = State()
    address_longitude = State()
    title = State()