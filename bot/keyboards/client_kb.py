from aiogram import types


class KeyboardClient:
    async def main_menu_ru(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Сделать заказ')
        btn2 = types.KeyboardButton('Расположение')
        btn3 = types.KeyboardButton('Информация')
        markup.add(btn1, btn2, btn3)
        return markup

    async def main_menu_en(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Make order')
        btn2 = types.KeyboardButton('Geo')
        btn3 = types.KeyboardButton('Info')
        markup.add(btn1, btn2, btn3)
        return markup

    async def menu_ru(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Бургеры')
        btn2 = types.KeyboardButton('Пицца')
        btn3 = types.KeyboardButton('Напитки')
        btn4 = types.KeyboardButton('Назад')
        markup.add(btn1, btn2, btn3, btn4)
        return markup

    async def menu_en(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Burgers')
        btn2 = types.KeyboardButton('Pizza')
        btn3 = types.KeyboardButton('Drinks')
        btn4 = types.KeyboardButton('Back')
        markup.add(btn1, btn2, btn3, btn4)
        return markup

    async def burgers(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Cheeseburger')
        btn2 = types.KeyboardButton('Chickenburger')
        btn3 = types.KeyboardButton('Bigmac')
        btn4 = types.KeyboardButton('Back')
        markup.add(btn1, btn2, btn3, btn4)
        return markup

    async def send_menu(self):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Add', callback_data='Add')
        btn2 = types.InlineKeyboardButton('Delete', callback_data='Delete')
        markup.add(btn1, btn2)
        return markup
