from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = KeyboardButton('/Add')
button_delete = KeyboardButton('/Delete')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete)
