from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    commands = [
            # BotCommand(command="start", description="Restart bot"),
            # BotCommand(command="help", description="Help info"),
            BotCommand(command="chat_info", description="Chat info"),
        ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
