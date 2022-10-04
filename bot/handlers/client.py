import types
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from db.repository import SqlRepository
from bot.keyboards.client_kb import KeyboardClient


class FSMClient(StatesGroup):
    menu = State()
    dish = State()
    send_menu = State()


class ClientHandlers:
    sqlRepository = SqlRepository()
    keyboardClient = KeyboardClient()

    async def start_command(self, message: types.Message, state: FSMContext):
        if await self.sqlRepository.user_language_code(message.from_user.id) == 'ru':
            await message.answer(
                f'Привет, {message.from_user.get_mention(as_html=True)}, '
                f'у нас ты можешь заказать самые вкусные бургеры',
                parse_mode=types.ParseMode.HTML,
                reply_markup=await self.keyboardClient.main_menu_ru(),
            )
        else:
            await message.answer(
                f'Hello, {message.from_user.get_mention(as_html=True)}, '
                f'here you can order the most delicious burgers',
                parse_mode=types.ParseMode.HTML,
                reply_markup=await self.keyboardClient.main_menu_en(),
            )
        if not await self.sqlRepository.is_user_exist(message.from_user.id):
            await self.sqlRepository.save_user(message.from_user.id, message.from_user.username,
                                               message.from_user.language_code)

    async def help_command(self, message: types.Message):
        if await self.sqlRepository.user_language_code(message.from_user.id) == 'ru':
            await message.answer(
                f'Привет, в этом боте ты можешь заказать самые вкусные бургеры в Ванадзоре'
            )
        else:
            await message.answer(
                f'Hello, here you can order the most delicious burgers in Vanadzor'
            )

    async def menu(self, message: types.Message):
        if await self.sqlRepository.user_language_code(message.from_user.id) == 'ru':
            await message.answer(
                f'Выбери категорию',
                reply_markup=await self.keyboardClient.menu_ru(),
            )
        else:
            await message.answer(
                f'Choose a category',
                reply_markup=await self.keyboardClient.menu_en(),
            )

    async def burgers(self, message: types.Message):
        markup = await self.keyboardClient.burgers()
        await message.answer(
            f'Choose a burger',
            reply_markup=markup,
        )

    async def pizza(self, message: types.Message):
        markup = await self.keyboardClient.pizza()
        await message.answer(
            f'Choose a pizza',
            reply_markup=markup,
        )

    async def drinks(self, message: types.Message):
        markup = await self.keyboardClient.drinks()
        await message.answer(
            f'Choose a drink',
            reply_markup=markup,
        )

    async def send_menu(self, message: types.Message):
        dishes = await self.sqlRepository.extract_menu(message.text)
        markup = await self.keyboardClient.send_menu()
        await message.answer_photo(
            dishes[1], f'Title: {dishes[2]}\nDescription: {dishes[4]}\nPrice: {dishes[5]}',
            reply_markup=markup,
        )

    def register_handler_client(self, dp: Dispatcher):
        dp.register_message_handler(
            self.start_command,
            commands=['start'],
        )
        dp.register_message_handler(
            self.help_command,
            commands=['help'],
        )
        dp.register_message_handler(
            self.menu,
            lambda message: ('Make order', 'Сделать заказ').__contains__(message.text),
        )
        dp.register_message_handler(
            self.burgers,
            lambda message: ('Burgers', 'Бургеры').__contains__(message.text),
        )
        dp.register_message_handler(
            self.pizza,
            lambda message: 'Pizza'.__contains__(message.text),
        )
        dp.register_message_handler(
            self.burgers,
            lambda message: 'Drink'.__contains__(message.text),
        )
        dp.register_message_handler(
            self.send_menu,
            lambda message: ('Cheeseburger', 'Chickenburger', 'Bigmac').__contains__(message.text),
        )
