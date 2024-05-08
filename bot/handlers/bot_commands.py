from werkzeug.security import generate_password_hash
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import displaySelectLanguageMenu, sendPhoneNumber, displayGeneralMenu
from utils.registration import Form
from globalVariables import globalVariables
from translate import translate as ts

from datebase.adminFuncs import addAdmin
from datebase.user import regUser, getLang, isReg

router = Router()

@router.message(CommandStart())
async def cmdStart(message: Message, state: FSMContext):
    try:
        if not await isReg(message.from_user.id):
            await state.set_state(Form.lang)
            await message.answer("Hello, choose a language.", reply_markup=displaySelectLanguageMenu())
        else:
            await message.answer(ts("Ви вже зареєстровані.", await getLang(message.from_user.id)))
    except Exception as err:
            print(err)

@router.message(Command('giveadmin'))
async def command_handler(message: Message):
    try:
        if message.from_user.id in globalVariables.adminList:
            command_args = message.text.split()[1:]  # Исключаем первый элемент, так как это сама команда
            print(len(command_args))
            if len(command_args) == 2:
                login = command_args[0]
                password = generate_password_hash(command_args[1])

                await addAdmin(login, password)
                await message.answer(f"На сайті надано адмін-права новому акаунту\nLogin: {login}\nHashed passwd: {password}")
    except Exception as err:
        print(err)

@router.message(Form.lang)
async def form_lang(message: Message, state: FSMContext):
    try:
        if message.text == 'English' or message.text == 'Українська':
            await state.update_data(lang=message.text)
            await state.set_state(Form.phoneNumber)
            await message.answer("Language selection is successful, now share your authorization number.", reply_markup=sendPhoneNumber())
    except Exception as err:
            print(err)

@router.message(Form.phoneNumber)
async def form_number(message: Message, state: FSMContext):
    try:
        if message.contact and message.contact.user_id == message.from_user.id:
            await state.update_data(phoneNumber=message.contact.phone_number)
            data = await state.get_data()
            if data['lang'] == 'English':
                lang = 'en'
            elif data['lang'] == 'Українська':
                 lang = 'ukr'
            phoneNumber = data['phoneNumber']
            await regUser(message.chat.id, phoneNumber, lang)
            await state.clear()
            await message.answer(f"{ts("Реєстрація пройшла успішно.", await getLang(message.from_user.id))}\n{ts("Ви успішно перейшли в головне меню.", await getLang(message.from_user.id))}", reply_markup=await displayGeneralMenu(message.from_user.id))
        else:
            await message.answer("You did not share a contact, please try again.")
    except Exception as err:
            print(err)