import logging
import config
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from db.repository import SqlRepository
from aiogram.utils.executor import start_webhook
from aiogram import types

sqlRepository = SqlRepository()


class UserState(StatesGroup):
    main_menu = State()
    order = State()
    address = State()


async def on_startup(dispatcher):
    await config.bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await config.bot.delete_webhook()


@config.dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not sqlRepository.is_user_exist(message.from_user.id):
        sqlRepository.save_user(message.from_user.id, message.from_user.username, message.from_user.language_code)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Make order')
    btn2 = types.KeyboardButton('Contacts')
    btn3 = types.KeyboardButton('Info')
    markup.add(btn1, btn2, btn3)
    if message.from_user.language_code == 'ru':
        await message.answer(
            f'Привет, {message.from_user.get_mention(as_html=True)}, у нас ты можешь заказать самые вкусные бургеры',
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup
        )
    elif message.from_user.language_code == 'en':
        await message.answer(
            f'Hello, {message.from_user.get_mention(as_html=True)}, here you can order the most delicious burgers',
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup
        )


@config.dp.message_handler(commands=['Make order'])
async def make_order(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Burgers')
    btn2 = types.KeyboardButton('Pizza')
    btn3 = types.KeyboardButton('Salads')
    btn4 = types.KeyboardButton('Drinks')
    btn5 = types.KeyboardButton('My order')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    await message.answer(
        'Choose dishes',
        reply_markup=markup
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=config.dp,
        webhook_path=config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )
