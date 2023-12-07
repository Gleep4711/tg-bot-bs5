# from asyncio import sleep
# from textwrap import dedent
# import re

from aiogram import Router
# from aiogram.dispatcher.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.methods.forward_message import ForwardMessage

# from bot.const import START_POINTS, STICKER_FAIL, SPIN_TEXT, THROTTLE_TIME_SPIN
# from bot.dice_check import get_combo_data
# from bot.keyboards import get_debug_keyboard, get_start_keyboard
# from bot.sql import users, connect
# from bot.utilits import debug, log, update
# from bot.const import RESTART_PROGRESS_TEXT
from bot.config_reader import config

# flags = {"throttling_key": "spin"}
router = Router()

@router.message()
async def all_message(message: Message, state: FSMContext):
    return # Ничего не делаем
    # Если команда неизвестная - сообщаем об ошибке 
    await message.answer('Что-то пошло не так...')
    await ForwardMessage(chat_id=config.logs_error_channel_id, from_chat_id=message.chat.id, message_id=message.message_id)
