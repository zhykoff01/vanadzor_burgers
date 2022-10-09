import types
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from db.repository import SqlRepository
from bot.keyboards.client_kb import KeyboardClient


class FSMClient(StatesGroup):
    state_phone_number = State()
    state_menu = State()
    state_second_menu = State()
    state_food = State()
    state_send_menu = State()


class ClientHandlers:
    sqlRepository = SqlRepository()
    keyboardClient = KeyboardClient()

    # async def main_menu(self, message: types.Message, state: FSMContext):
    #     current_state = await state.get_state()
    #     if current_state is None:
    #         return
    #     await state.finish()

    # async def back(self, message: types.Message, state: FSMContext):
    #     user_position = await state.get_state()
    #     if user_position is None:
    #         return
    #     if user_position is FSMClient.state_menu:
    #         await state.finish()
    #         await self.start_command(message)
    #     elif user_position:
    #         pass

    async def start_command(self, message: types.Message):
        if await self.sqlRepository.user_language_code(message.from_user.id) == 'ru':
            await message.answer(
                f'Привет, {message.from_user.get_mention(as_html=True)}, '
                f'у нас ты можешь заказать самые вкусные бургеры.',
                parse_mode=types.ParseMode.HTML,
            )
            await message.answer(
                f'Пожалуйста, введите свой номер телефона, чтобы зарегистрироваться!'
                f'Например, +374 xx xxxxxx',
                reply_markup=await self.keyboardClient.send_phone_number(),
            )
        else:
            await message.answer(
                f'Hello, {message.from_user.get_mention(as_html=True)}, '
                f'here you can order the most delicious burgers.',
                parse_mode=types.ParseMode.HTML,
            )
            await message.answer(
                f'Please enter your phone number to register!'
                f'For example, +374 xx xxxxxx',
                reply_markup=await self.keyboardClient.send_phone_number(),
            )
        if not await self.sqlRepository.is_user_exist(message.from_user.id):
            await self.sqlRepository.save_user(message.from_user.id, message.from_user.username,
                                               message.from_user.language_code)
        await FSMClient.state_phone_number.set()

    async def phone_number(self, message: types.Message, state: FSMContext):
        await self.sqlRepository.save_phone_number(message.text.strip(), message.from_user.id)
        user = await self.sqlRepository.extract_user(message.from_user.id)
        await message.answer(
            f'You are registered,\n'
            f'your id = {user[0]},\n'
            f'your user id = {user[1]},\n'
            f'your username = {user[2]},\n'
            f'your language code = {user[3]},\n'
            f'your phone number = {user[4]}.',
            reply_markup=await self.keyboardClient.send_phone_number(),
        )
        await FSMClient.state_menu.set()

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
        await FSMClient.state_second_menu.set()

    async def burgers(self, message: types.Message):
        markup = await self.keyboardClient.burgers()
        await message.answer(
            f'Choose a burger',
            reply_markup=markup,
        )
        await FSMClient.state_food.set()

    async def pizza(self, message: types.Message):
        markup = await self.keyboardClient.pizza()
        await message.answer(
            f'Choose a pizza',
            reply_markup=markup,
        )
        await FSMClient.state_food.set()

    async def drinks(self, message: types.Message):
        markup = await self.keyboardClient.drinks()
        await message.answer(
            f'Choose a drink',
            reply_markup=markup,
        )
        await FSMClient.state_food.set()

    async def send_menu(self, message: types.Message):
        dishes = await self.sqlRepository.extract_menu(message.text)
        markup = await self.keyboardClient.send_menu()
        await message.answer_photo(
            dishes[1], f'Title: {dishes[2]}\nDescription: {dishes[4]}\nPrice: {dishes[5]}',
            reply_markup=markup,
        )

    async def filter(self, message: types.Message):
        markup = await self.keyboardClient.filter()
        await message.answer(
            f'Send "start" to continue',
            reply_markup=markup,
        )

    def register_handler_client(self, dp: Dispatcher):
        dp.register_message_handler(
            self.start_command,
            commands=('start', 'help'),
            state='*',
        )
        dp.register_message_handler(
            self.phone_number,
            lambda message: message.text.startswith('+374'),
            state=FSMClient.state_phone_number,
        )
        dp.register_message_handler(
            self.menu,
            lambda message: ('Make order', 'Сделать заказ').__contains__(message.text),
            state=FSMClient.state_menu,
        )
        dp.register_message_handler(
            self.burgers,
            lambda message: ('Burgers', 'Бургеры').__contains__(message.text),
            state=FSMClient.state_second_menu,
        )
        dp.register_message_handler(
            self.pizza,
            lambda message: 'Pizza'.__contains__(message.text),
            state=FSMClient.state_second_menu,
        )
        dp.register_message_handler(
            self.drinks,
            lambda message: 'Drink'.__contains__(message.text),
            state=FSMClient.state_second_menu,
        )
        dp.register_message_handler(
            self.send_menu,
            lambda message: ('Cheeseburger', 'Chickenburger', 'Bigmac').__contains__(message.text),
            state=FSMClient.state_food,
        )
        dp.register_message_handler(
            self.filter,
        )
