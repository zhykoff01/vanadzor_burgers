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
