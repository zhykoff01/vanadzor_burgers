from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot.config import ADMIN_ID
from db.repository import SqlRepository
from bot.keyboards import admin_kb


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    section = State()
    description = State()
    price = State()


class AdminHandlers:
    sqlRepository = SqlRepository()
    ID = ADMIN_ID

    async def cancel_handler(self, message: types.Message, state: FSMContext):
        if message.from_user.id == self.ID:
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await message.reply('OK')

    async def admin(self, message: types.Message):
        if message.from_user.id == self.ID:
            await message.reply('Admin panel', reply_markup=admin_kb.button_case_admin)

    async def add(self, message: types.Message):
        if message.from_user.id == self.ID:
            await FSMAdmin.photo.set()
            await message.reply('Download photo')

    async def load_photo(self, message: types.Message, state: FSMContext):
        if message.from_user.id == self.ID:
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            await FSMAdmin.next()
            await message.reply('Enter a title')

    async def load_name(self, message: types.Message, state: FSMContext):
        if message.from_user.id == self.ID:
            async with state.proxy() as data:
                data['name'] = message.text
            await FSMAdmin.next()
            await message.reply('Enter section')

    async def load_section(self, message: types.Message, state: FSMContext):
        if message.from_user.id == self.ID:
            async with state.proxy() as data:
                data['section'] = message.text
            await FSMAdmin.next()
            await message.reply('Enter description')

    async def load_description(self, message: types.Message, state: FSMContext):
        if message.from_user.id == self.ID:
            async with state.proxy() as data:
                data['description'] = message.text
            await FSMAdmin.next()
            await message.reply('Enter price')

    async def load_price(self, message: types.Message, state: FSMContext):
        if message.from_user.id == self.ID:
            async with state.proxy() as data:
                data['price'] = int(message.text)
            await self.sqlRepository.save_dishes(state)
            await message.reply(f'Saved successfully: {data}')
            await state.finish()

    def register_handler_admin(self, dp: Dispatcher):
        dp.register_message_handler(self.cancel_handler, state='*', commands='Cancel')
        dp.register_message_handler(self.cancel_handler, Text(equals='Cancel', ignore_case=True), state='*')
        dp.register_message_handler(self.admin, commands='Admin')
        dp.register_message_handler(self.add, commands='Add', state=None)
        dp.register_message_handler(self.load_photo, content_types='photo', state=FSMAdmin.photo)
        dp.register_message_handler(self.load_name, state=FSMAdmin.name)
        dp.register_message_handler(self.load_section, state=FSMAdmin.section)
        dp.register_message_handler(self.load_description, state=FSMAdmin.description)
        dp.register_message_handler(self.load_price, state=FSMAdmin.price)
