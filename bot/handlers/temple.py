# from asyncio import sleep
# from textwrap import dedent
# import re

from aiogram import Router, F
# from aiogram.dispatcher.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.methods.forward_message import ForwardMessage
# from aiogram.filters.text import Text

# from bot.const import START_POINTS, STICKER_FAIL, SPIN_TEXT, THROTTLE_TIME_SPIN
# from bot.dice_check import get_combo_data
# from bot.keyboards import get_debug_keyboard, get_start_keyboard
# from bot.sql import users, connect
# from bot.utilits import debug, log, update
# from bot.const import RESTART_PROGRESS_TEXT
from bot.config_reader import config
import re

# flags = {"throttling_key": "spin"}
router = Router()
old_temple_id = 558306816

@router.message((F.forward_from.id == old_temple_id) & (F.text.contains('Корабельный экипаж')))
async def temple_message(message: Message, state: FSMContext):
    data = {
        'gang': 'Оружейники:\n',
        'matros': 'Матросы:\n',
        'diver': 'Пловцы:\n',
        'pirate': 'Пираты:\n',
    }
    for s in message.text.split('\n'):
        if s.startswith('Оружейник'):
            name, hp, s1, s2 = re.findall(r'Оружейник (\w* \w*) \d*/(\d*)\D*(\d*)\D*(\d*)', s).pop()
            data['gang'] += '{} {}hp {}'.format(name, hp, int(s1) + int(s2)) + '\n'
        if s.startswith('Матрос'):
            name, hp, s1, s2 = re.findall(r'Матрос (\w* \w*) \d*/(\d*)\D*(\d*)\D*(\d*)', s).pop()
            data['matros'] += '{} {}hp {}'.format(name, hp, int(s1) + int(s2)) + '\n'
        if s.startswith('Пловец'):
            name, hp, s1, s2 = re.findall(r'Пловец (\w* \w*) \d*/(\d*)\D*(\d*)\D*(\d*)', s).pop()
            data['diver'] += '{} {}hp {}'.format(name, hp, int(s1) + int(s2)) + '\n'
        if s.startswith('Пират'):
            name, hp, s1, s2 = re.findall(r'Пират (\w* \w*) \d*/(\d*)\D*(\d*)\D*(\d*)', s).pop()
            data['pirate'] += '{} {}hp {}'.format(name, hp, int(s1) + int(s2)) + '\n'
    msg = '{}\n{}\n{}\n{}'.format(data['gang'], data['matros'], data['diver'], data['pirate'])

    await message.answer('{}'.format(msg))

# from aiogram.handlers import MessageHandler
# @router.message()
# class MyHandler(MessageHandler):
#     async def handle(self) -> Any:
#         return SendMessage(chat_id=self.chat.id, text="PASS")