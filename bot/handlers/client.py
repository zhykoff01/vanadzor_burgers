import types
from aiogram import types, Dispatcher
from bot.main import sqlRepository


async def start(message: types.Message):
    if not sqlRepository.is_user_exist(message.from_user.id):
        sqlRepository.save_user(message.from_user.id, message.from_user.username, message.from_user.language_code)
    if message.from_user.language_code == 'ru':
        await message.answer(
            f'Привет, {message.from_user.get_mention(as_html=True)}, у нас ты можешь заказать самые вкусные бургеры',
            parse_mode=types.ParseMode.HTML,
        )
    elif message.from_user.language_code == 'en':
        await message.answer(
            f'Hello, {message.from_user.get_mention(as_html=True)}, here you can order the most delicious burgers',
            parse_mode=types.ParseMode.HTML,
        )


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
