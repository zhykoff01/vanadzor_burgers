import types
from aiogram import types, Dispatcher
from db.repository import SqlRepository
from bot.config import bot


sqlRepository = SqlRepository()


async def start_command(message: types.Message):
    if not sqlRepository.is_user_exist(message.from_user.id):
        await sqlRepository.save_user(message.from_user.id, message.from_user.username, message.from_user.language_code)
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


async def help_command(message: types.Message):
    if message.from_user.language_code == 'ru':
        await message.answer(
            f'Привет, в этом боте ты можешь заказать самые вкусные бургеры в Ванадзоре'
        )
    elif message.from_user.language_code == 'en':
        await message.answer(
            f'Hello, here you can order the most delicious burgers in Vanadzor'
        )


async def send_menu(message: types.Message):
    if message.from_user == 'Pizza':
        some_response = sqlRepository.extract_dishes(message.from_user)
        for res in await some_response:
            await bot.send_photo(message.from_user.id, res[0], f'{res[1]}\nDescription: {res[2]}\nPrice: {res[-1]}')


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
