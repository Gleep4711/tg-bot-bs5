import asyncio
import logging

from aiogram.types import ReplyKeyboardRemove

from bot.bot import bot, dp
from bot.config_reader import config
from bot.handlers import (admin_commands, bastion_forward, callbacks,
                          default_commands, echo, temple)
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.ui_commands import set_bot_commands


async def main():
    logging.basicConfig(level=logging.CRITICAL)

    dp.include_router(default_commands.router)
    dp.include_router(admin_commands.router)
    dp.include_router(temple.router)
    dp.include_router(bastion_forward.router)
    dp.include_router(echo.router)

    dp.include_router(callbacks.router)

    dp.message.middleware(ThrottlingMiddleware())

    await set_bot_commands(bot)

    try:
        await bot.send_message(chat_id=config.bots_manager_group_id_main_chat, text='Bot launcher', reply_markup=ReplyKeyboardRemove())
        # await bot.send_message(chat_id=config.admin, text='Bot launcher', reply_markup=ReplyKeyboardRemove()) # debug
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
