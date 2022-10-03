import logging
import config
from aiogram.utils.executor import start_webhook
from handlers.client import ClientHandlers
from handlers.admin import AdminHandlers
from config import dp

clientHandlers = ClientHandlers()
adminHandlers = AdminHandlers()


async def on_startup(dispatcher):
    await config.bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await config.bot.delete_webhook()


clientHandlers.register_handler_client(dp)
adminHandlers.register_handler_admin(dp)


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
