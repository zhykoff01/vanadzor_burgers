import logging
import config
from db.repository import SqlRepository
from aiogram.utils.executor import start_webhook
from aiogram import types

sqlRepository = SqlRepository()


async def on_startup(dispatcher):
    await config.bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await config.bot.delete_webhook()


@config.dp.message_handler()
async def start(message: types.Message):
    if not sqlRepository.is_user_exist(message.from_user.id):
        await sqlRepository.save_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f'Suck some dick, {message.from_user.get_mention(as_html=True)}',
        parse_mode=types.ParseMode.HTML,
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=config.dp,
        webhook_path=config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )
