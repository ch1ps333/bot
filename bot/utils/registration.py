from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    lang = State()
    phoneNumber = State()
    changelang = State()