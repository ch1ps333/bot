from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from translate import translate as ts
from datebase.user import getLang

def displaySelectLanguageMenu():
    langKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="English"),
                KeyboardButton(text="Українська")
            ],
        ],
        resize_keyboard=True
    )

    return langKeyboard

def sendPhoneNumber():
    getNumberKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Send phone number", request_contact=True),
            ],
        ],
        resize_keyboard=True, one_time_keyboard=True
    )

    return getNumberKeyboard

async def displayGeneralMenu(tgId):
    generalMenuKeyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ts("Профіль", await getLang(tgId)))
            ],
            [
                KeyboardButton(text=ts("Змінити мову", await getLang(tgId))),
                KeyboardButton(text=ts("Вийти з кабінету", await getLang(tgId)))
            ]
        ],
        resize_keyboard=True
    )
    return generalMenuKeyboard