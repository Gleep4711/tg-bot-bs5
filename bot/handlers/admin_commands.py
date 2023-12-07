import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.config_reader import config

router = Router()

@router.message((F.text == '/restart_bot_please') & (F.from_user.id == config.admin))
async def restart_bot(message: Message):
    exit()

