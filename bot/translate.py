translations = {
    'en': {
        "Ви вже зареєстровані.": "You are already registered.",
        "Реєстрація пройшла успішно.": "Registration was successful.",
        "Ви успішно перейшли в головне меню.": "You have successfully entered the main menu.",
        "У вас нема облікового запису в базі даних.": "You do not have an account in the database.",
        "Інформація про ваш особистий кабінет: ": "Information about your personal account: ",
        "Ім'я: ": 'Name: ',
        "Номер телефону: ": "Phone number: ",
        'Баланс: ': 'Balance: ',
        "Тип підписки: ": "Subscription type: ",
        "Дата закінчення підписки: ": "Subscription end date: ",
        "Виберіть мову.": "Choose language.",
        "Ви успішно вийшли з облікового запису, щоб авторизуватись повторно, введіть /start.": "You have successfully logged out, to log in again, type /start.",
        'Профіль': 'Profile',
        "Змінити мову": "Change language",
        "Вийти з кабінету": 'Logout',
    }
}

def translate(text, lang):
    if lang == 'ukr':
        return text
    else:
        global translations
        try:
            return translations[lang][text]
        except:
            return text
