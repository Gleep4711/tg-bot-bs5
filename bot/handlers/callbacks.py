import json

from aiogram import Router
from aiogram.types import CallbackQuery

from bot.bot import bot
from bot.common import BastionInlineDynamic
from bot.users import users_topics

router = Router(name='callbacks-router')


@router.callback_query(BastionInlineDynamic.filter())
async def bastion_callback_forward(callback: CallbackQuery):
    text = callback.data.split(':')
    data = {
        'id': callback.message.text,
        'callback': text[1],
    }
    await bot.send_message(users_topics[callback.message.message_thread_id]['id'], json.dumps(data))
