from aiogram import types


class KeyboardClient:
    def __init__(self, bot):
        self.bot = bot

    async def main_menu(self, message):
        markup_en = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_ru = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_en = types.KeyboardButton('Make order')
        btn2_en = types.KeyboardButton('Geo')
        btn3_en = types.KeyboardButton('Info')
        btn1_ru = types.KeyboardButton('Сделать заказ')
        btn2_ru = types.KeyboardButton('Расположение')
        btn3_ru = types.KeyboardButton('Информация')
        markup_en.add(btn1_en, btn2_en, btn3_en)
        markup_ru.add(btn1_ru, btn2_ru, btn3_ru)
        if message.from_user.language_code == 'ru':
            await message.answer(
                f'Привет, {message.from_user.get_mention(as_html=True)}, '
                f'у нас ты можешь заказать самые вкусные бургеры',
                parse_mode=types.ParseMode.HTML,
                reply_markup=markup_ru,
            )
        else:
            await message.answer(
                f'Hello, {message.from_user.get_mention(as_html=True)}, '
                f'here you can order the most delicious burgers',
                parse_mode=types.ParseMode.HTML,
                reply_markup=markup_en,
            )
