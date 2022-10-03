import types
from aiogram import types, Dispatcher
from db.repository import SqlRepository
from bot.keyboards.client_kb import KeyboardClient
from bot.config import bot


sqlRepository = SqlRepository()
keyboardClient = KeyboardClient()


async def start_command(message: types.Message):
    if message.from_user.language_code == 'ru':
        markup = await keyboardClient.main_menu_ru()
        await message.answer(
            f'Привет, {message.from_user.get_mention(as_html=True)}, '
            f'у нас ты можешь заказать самые вкусные бургеры',
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup,
        )
    else:
        markup = await keyboardClient.main_menu_en()
        await message.answer(
            f'Hello, {message.from_user.get_mention(as_html=True)}, '
            f'here you can order the most delicious burgers',
            parse_mode=types.ParseMode.HTML,
            reply_markup=markup,
        )
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
    if message.from_user.language_code == 'ru':
        markup = await keyboardClient.menu_ru()
        await message.answer(
            f'Выбери категорию',
            reply_markup=markup,
        )
    else:
        markup = await keyboardClient.menu_en()
        await message.answer(
            f'Choose a category',
            reply_markup=markup,
        )


async def burgers(message: types.Message):
    markup = await keyboardClient.burgers()
    await message.answer(
        f'Choose a burger',
        reply_markup=markup,
    )


async def send_menu(message: types.Message):
    dishes = await sqlRepository.extract_menu(message.text)
    markup = await keyboardClient.send_menu()
    await message.answer_photo(
        dishes[1], f'Title: {dishes[2]}\nDescription: {dishes[4]}\nPrice: {dishes[5]}',
        reply_markup=markup,
    )


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(menu, lambda message: ('Make order', 'Сделать заказ').__contains__(message.text))
    dp.register_message_handler(burgers, lambda message: ('Burgers', 'Бургеры').__contains__(message.text))
    dp.register_message_handler(
        send_menu, lambda message: ('Cheeseburger', 'Chickenburger', 'Bigmac').__contains__(message.text)
    )
