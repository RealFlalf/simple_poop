import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
import sqlite3
import db

# Bot token can be obtained via https://t.me/BotFather
load_dotenv()

TOKEN = getenv("BOT_TOKEN")
# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command('register'))
async def register_handler(message: Message) -> None:
    user = message.from_user
    try:
        connection = sqlite3.connect('simple_poop.db')
        courcor = connection.cursor()
        courcor.execute(f'''INSERT INTO Score (first_name, username, score) 
                        VALUES ('{user.first_name}', '{user.username}', 0)''')
        connection.commit()
        connection.close()
    except sqlite3.IntegrityError as e:
        await message.answer(f'Пользователь уже зарегестрирован')
        connection.close()
        return
    await message.answer(f"Пользователь {user.username} успешно подключен к игре!")


@dp.message(Command('plus'))
async def plus_handler(message: Message) -> None:
    user = message.from_user
    try:
        connection = sqlite3.connect('simple_poop.db')
        courcor = connection.cursor()
        courcor.execute(f'''SELECT * FROM Score where username = "{user.username}"''')
        user_db = courcor.fetchone()
        if not user_db:
            await message.answer(f'Пользователь {user.username} не найден! Сначала нужно зарегестрироваться /register')
            connection.close()
            return
        new_score = user_db[3] + 1
        courcor.execute(f'''UPDATE Score SET score = {new_score} WHERE username = "{user.username}"''')
        connection.commit()
        connection.close()
    except Exception as e:
        await message.answer(f'Что-то пошло не так :(\n {e}')
        connection.close()
        return
    await message.answer(f'Поздравляю с покаком, {user.username}! Надеюсь он был хороший!')


@dp.message(Command('top'))
async def top_handler(message: Message) -> None:
    try:
        connection = sqlite3.connect('simple_poop.db')
        courcor = connection.cursor()
        courcor.execute(f'''SELECT * FROM Score ORDER BY score DESC''')
        scores = courcor.fetchall()
        result = ['Топ игроков:']
        for idx, score in enumerate(scores):
            result.append(f'{idx+1}. {score[1]}: {score[3]}')
        connection.close()
    except Exception as e:
        await message.answer(f'Что-то пошло не так :(\n {e}')
        connection.close()
        return
    result = '\n'.join(result)
    await message.answer(result)

@dp.message(Command('score'))
async def score_handler(message: Message) -> None:
    user = message.from_user
    try:
        connection = sqlite3.connect('simple_poop.db')
        courcor = connection.cursor()
        courcor.execute(f'''SELECT * FROM Score where username = "{user.username}"''')
        user_db = courcor.fetchone()
        score = user_db[3]
        connection.close()
    except Exception as e:
        await message.answer(f'Что-то пошло не так :(\n {e}')
        return
    await message.answer(f'Ваш счет {score}. Неплохой результат')


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())