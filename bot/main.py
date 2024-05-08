from aiogram import Bot, Dispatcher

import subprocess
from aiogram.client.session.aiohttp import AiohttpSession

from handlers import bot_commands, bot_user_messages
from config import config as cfg

from datebase.adminFuncs import getAdminList

from globalVariables import globalVariables

import asyncio
import multiprocessing
import os

def run_flask_server():
    current_directory = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_directory, '..'))
    pt = f"{project_root}/www/"
    path = os.path.join(project_root, 'www', 'app.py')
    subprocess.run(['python', '-m', 'flask', 'run'], cwd=pt)


def start_bot():
    asyncio.run(main())

async def main():
    bot = Bot(cfg.bot_token.get_secret_value())
    dp = Dispatcher()

    globalVariables.adminList = await getAdminList()

    dp.include_routers (
        bot_commands.router,
        bot_user_messages.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    #flask_process = multiprocessing.Process(target=run_flask_server)
    bot_process = multiprocessing.Process(target=start_bot)

    # Запуск процессов
    #flask_process.start()
    bot_process.start()

    # Ожидание завершения процессов
    #flask_process.join()
    bot_process.join()