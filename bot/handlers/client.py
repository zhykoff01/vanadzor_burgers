import types
from aiogram import types, Dispatcher
from aiogram.utils.callback_data import CallbackData
from db.repository import SqlRepository
from bot.config import bot


sqlRepository = SqlRepository()


async def start_command(message: types.Message):
    markup_en, markup_ru = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_en = types.KeyboardButton('Make order')
    btn2_en = types.KeyboardButton('Geo')
    btn3_en = types.KeyboardButton('Info')
    btn1_ru = types.KeyboardButton('Сделать заказ')
    btn2_ru = types.KeyboardButton('Расположение')
    btn3_ru = types.KeyboardButton('Информация')
    markup_en.add(btn1_en, btn2_en, btn3_en)
    markup_ru.add(btn1_ru, btn2_ru, btn3_ru)
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
    some_response = await sqlRepository.extract_menu(message)
    for res in some_response:
        await bot.send_photo(message.from_user.id, res[0], f'{res[1]}\nDescription: {res[3]}\nPrice: {res[-1]}')


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(send_menu, commands=['pizza'])
