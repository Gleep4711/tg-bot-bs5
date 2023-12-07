import json

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.methods.forward_message import ForwardMessage
from aiogram.types import Message, ReplyKeyboardRemove
from bot.bot import bot
from bot.config_reader import config
from bot.keyboards import build_keyboard, build_inline
from bot.users import users_ids, users_topics

ids = set()
for user_id in users_ids:
    ids.add(user_id)

router = Router()

@router.message((F.forward_from.id == config.bs_id) & (F.chat.type == 'private'))
async def bastion_forward(message: Message, state: FSMContext):
    await bot.forward_message(
        chat_id=config.bots_manager_group_id_main_chat,
        message_thread_id=users_ids[message.from_user.id]['topic'],
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

@router.message((F.from_user.id.in_(ids)) & (F.chat.type == 'private'))
async def private_user_bots(message: Message, state: FSMContext):
    message_thread_id = users_ids[message.from_user.id]['topic']

    if message.text.startswith('{'):
        data = json.loads(message.text)
        if 'keyboard' in data:
            await bot.send_message(
                chat_id=config.bots_manager_group_id_main_chat,
                message_thread_id=message_thread_id,
                text='...',
                reply_markup=build_keyboard(data['keyboard']),
            )
        elif 'inline_keyboard' in data:
            await bot.send_message(
                chat_id=config.bots_manager_group_id_main_chat,
                message_thread_id=message_thread_id,
                text='{}@{}'.format(message.from_user.id, data['message_id'] or '...'),
                reply_markup=build_inline(data['inline_keyboard']),

            )

    else:
        await bot.forward_message(
            chat_id=config.bots_manager_group_id_main_chat,
            message_thread_id=message_thread_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )

@router.message((F.chat.id == config.bots_manager_group_id_main_chat))
async def bots_manager_group(message: Message, state: FSMContext):
    ''' We send messages to the user '''
    if not message.text or not (message.message_thread_id in users_topics):
        return

    msg = message.text
    if '@' in msg:
        msg = msg[:msg.find('@')]
    if 'http' in msg.lower():
        msg = msg[:msg.lower().find('http')]
    if not msg:
        return

    excludes = ['/chat_info', 'test']
    if msg.lower() in excludes or msg.startswith('http'):
        await message.answer('Не надо так делать...')
        return

    if msg.lower() in ['/dig', '/hunt']:
        await message.answer('Спасибо, но с этим я сам как нибудь справлюсь, ты лучше пофарми немного.')
        return

    await bot.send_message(chat_id=users_topics[message.message_thread_id]['id'], text=msg)
    # await bot.forward_message(chat_id=users_topics[message.message_thread_id]['id'], from_chat_id=message.chat.id, message_id=message.message_id)