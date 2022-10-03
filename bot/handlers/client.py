import types
from aiogram import types, Dispatcher
from db.repository import SqlRepository
from bot.keyboards.client_kb import KeyboardClient


sqlRepository = SqlRepository()


async def start_command(message: types.Message):
    await KeyboardClient.main_menu(message.text)
    if not await sqlRepository.is_user_exist(message.from_user.id):
        await sqlRepository.save_user(message.from_user.id, message.from_user.username, message.from_user.language_code)


async def help_command(message: types.Message):
    if message.from_user.language_code == 'ru':
        await message.answer(
            f'Привет, в этом боте ты можешь заказать самые вкусные бургеры в Ванадзоре'
        )
    else:
        await message.answer(
            f'Hello, here you can order the most delicious burgers in Vanadzor'
        )


async def menu(message: types.Message):
    markup_en = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup_ru = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_en = types.KeyboardButton('Burgers')
    btn2_en = types.KeyboardButton('Pizza')
    btn3_en = types.KeyboardButton('Drinks')
    btn1_ru = types.KeyboardButton('Бургеры')
    btn2_ru = types.KeyboardButton('Пицца')
    btn3_ru = types.KeyboardButton('Напитки')
    markup_en.add(btn1_en, btn2_en, btn3_en)
    markup_ru.add(btn1_ru, btn2_ru, btn3_ru)
    if message.from_user.language_code == 'ru':
        await message.answer(
            f'Выбери категорию',
            reply_markup=markup_ru,
        )
    else:
        await message.answer(
            f'Choose a category',
            reply_markup=markup_en,
        )


async def burgers(message: types.Message):
    markup_en = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Cheeseburger')
    btn2 = types.KeyboardButton('Chickenburger')
    btn3 = types.KeyboardButton('Bigmac')
    markup_en.add(btn1, btn2, btn3)
    await message.answer(
        f'Choose a burger',
        reply_markup=markup_en,
    )


async def send_menu(message: types.Message):
    dishes = await sqlRepository.extract_menu(message.text)
    markup_en = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Add', callback_data='Add')
    btn2 = types.InlineKeyboardButton('Delete', callback_data='Delete')
    markup_en.add(btn1, btn2)
    await message.answer_photo(
        dishes[1], f'Title: {dishes[2]}\nDescription: {dishes[4]}\nPrice: {dishes[5]}',
        reply_markup=markup_en,
    )


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(menu, lambda message: ('Make order', 'Сделать заказ').__contains__(message.text))
    dp.register_message_handler(burgers, lambda message: ('Burgers', 'Бургеры').__contains__(message.text))
    dp.register_message_handler(
        send_menu, lambda message: ('Cheeseburger', 'Chickenburger', 'Bigmac').__contains__(message.text)
    )
    # dp.register_message_handler(send_menu, commands=['pizza'])
