from aiogram.dispatcher.filters.state import State, StatesGroup

class SignUpState(StatesGroup):
    name = State()
    tel = State()
    address_latitude = State()
    address_longitude = State()
    title = State()
class PhoneState(StatesGroup):
    phone = State()
class LocationState(StatesGroup):
    address_latitude = State()
class LocationState2(StatesGroup):
    address_longitude = State()