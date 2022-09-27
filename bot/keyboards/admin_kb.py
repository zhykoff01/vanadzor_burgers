from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


button_load = KeyboardButton('/Add')
button_delete = KeyboardButton('/Delete')
button_cancel = KeyboardButton('/Cancel')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load, button_delete, button_cancel)
