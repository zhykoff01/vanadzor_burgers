from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot.config import ID
from db.repository import SqlRepository
from bot.keyboards import admin_kb


sqlRepository = SqlRepository()


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    section = State()
    description = State()
    price = State()


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


async def admin(message: types.Message):
    if message.from_user.id == ID:
        await message.reply('Admin panel', reply_markup=admin_kb.button_case_admin)


async def add(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Download photo')


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Enter a title')


async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Enter section')


async def load_section(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['section'] = message.text
        await FSMAdmin.next()
        await message.reply('Enter description')


async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Enter price')


async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await sqlRepository.save_dishes(state)
        await message.reply(f'Saved successfully: {data}')
        await state.finish()


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', commands='Cancel')
    dp.register_message_handler(admin, commands='Admin')
    dp.register_message_handler(cancel_handler, Text(equals='Cancel', ignore_case=True), state='*')
    dp.register_message_handler(add, commands='Add', state=None)
    dp.register_message_handler(load_photo, content_types='photo', state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_section, state=FSMAdmin.section)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)