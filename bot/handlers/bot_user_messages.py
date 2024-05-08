from werkzeug.security import generate_password_hash

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from utils.registration import Form
from globalVariables import globalVariables
from translate import translate as ts
from datebase.adminFuncs import addAdmin
from datebase.user import isReg, getLang, getUserInfo, changeLang, logout
from keyboards.reply import displaySelectLanguageMenu, displayGeneralMenu

router = Router()

@router.message((F.text.lower() == "профіль") | (F.text.lower() == "profile"))
async def profile(message: Message):
    try:
        userInfo = await getUserInfo(message.from_user.id)
        lang = await getLang(message.from_user.id)
        if userInfo is None:
            await message.answer(ts("У вас нема облікового запису в базі даних.", lang))
        else:
            await message.answer(f"{ts("Інформація про ваш особистий кабінет: ", lang)}\n\n"
                        f"{ts("Ім'я: ", lang)}{userInfo[0][1]}\n"
                        f"{ts("Номер телефону: ", lang)}{userInfo[0][2]}\n"
                        f"{ts("Баланс: ", lang)}{userInfo[0][3]}\n"
                        f"{ts("Тип підписки: ", lang)}{userInfo[0][4]}\n"
                        f"{ts("Дата закінчення підписки: ", lang)}{userInfo[0][5]}\n")
    except Exception as err:
        print(err)

@router.message((F.text.lower() == "змінити мову") | (F.text.lower() == "change language"))
async def change_name(message: Message, state: FSMContext):
    try:
        await state.set_state(Form.changelang)
        await message.answer(ts("Виберіть мову.", await getLang(message.from_user.id)), reply_markup=displaySelectLanguageMenu())
    except Exception as err:
        print(err)

@router.message((F.text.lower() == "вийти з кабінету") | (F.text.lower() == "logout"))
async def change_name(message: Message):
    try:
        await logout(message.from_user.id)
        await message.answer(ts("Ви успішно вийшли з облікового запису, щоб авторизуватись повторно, введіть /start.", await getLang(message.from_user.id)))
    except Exception as err:
        print(err)

@router.message((F.text.lower() == "giveadmin"))
async def giveadmin(message: Message):
    try:
        if message.from_user.id in globalVariables.adminList:
            command_args = message.split()
            print(len(command_args))
            if len(command_args) == 2:
                login = command_args[0]
                password = generate_password_hash(command_args[1])

                await addAdmin(login, password)
                await message.answer(f"На сайті надано адмін-права новому акаунту\nLogin: {login}\nHashed passwd: {password}")
        else:
            print("ne admin")
    except Exception as err:
        print(err)

@router.message(Form.changelang)
async def change_name_(message: Message, state: FSMContext):
    try:
        if message.text == 'English':
            lang = 'en'
        elif message.text == 'Українська':
            lang = 'ukr'
        await changeLang(message.from_user.id, lang)
        await message.answer(ts("Ви успішно перейшли в головне меню.", await getLang(message.from_user.id)), reply_markup=await displayGeneralMenu(message.from_user.id))
        await state.clear()
    except Exception as err:
        print(err)