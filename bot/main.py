import logging
import config
import asyncio
from aiogram.utils.executor import start_webhook
from handlers.client import Handlers
from handlers import admin
from config import dp

handlers = Handlers()


async def on_startup(dispatcher):
    await config.bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await config.bot.delete_webhook()


async def register_handlers():
    await handlers.register_handler_client(dp)
    admin.register_handler_admin(dp)


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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(register_handlers())
    loop.close()
