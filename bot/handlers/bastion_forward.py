import json

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.bot import bot
from bot.config_reader import config, users_ids, users_topics, kate_users_topics
from bot.keyboards import build_keyboard, build_inline

ids = set()
for user_id in users_ids:
    ids.add(user_id)

router = Router()
F: Message


@router.message((F.forward_from.id == config.bs_id) & (F.chat.type == 'private'))
async def bastion_forward(message: Message, state: FSMContext):
    await bot.forward_message(
        # chat_id=config.bots_manager_group_id_main_chat,
        chat_id=users_ids[message.from_user.id]['forum'],
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
                # chat_id=config.bots_manager_group_id_main_chat,
                chat_id=users_ids[message.from_user.id]['forum'],
                message_thread_id=message_thread_id,
                text='...',
                reply_markup=build_keyboard(data['keyboard']),
            )
        elif 'inline_keyboard' in data:
            await bot.send_message(
                # chat_id=config.bots_manager_group_id_main_chat,
                chat_id=users_ids[message.from_user.id]['forum'],
                message_thread_id=message_thread_id,
                text='{}@{}'.format(message.from_user.id,
                                    data['message_id'] or '...'),
                reply_markup=build_inline(data['inline_keyboard']),

            )

    else:
        await bot.forward_message(
            # chat_id=config.bots_manager_group_id_main_chat,
            chat_id=users_ids[message.from_user.id]['forum'],
            message_thread_id=message_thread_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )


@router.message((F.chat.id.in_({config.bots_manager_group_id_main_chat, config.bots_manager_kate})))
async def bots_manager_group(message: Message, state: FSMContext):
    ''' We send messages to the user '''
    if not (message.text and message.message_thread_id in users_topics and message.message_thread_id in kate_users_topics):
        return
    if message.message_thread_id in users_topics:
        chat_id = users_topics[message.message_thread_id]['id']
    elif message.message_thread_id in kate_users_topics:
        chat_id = kate_users_topics[message.message_thread_id]['id']
    else:
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

    await bot.send_message(chat_id=chat_id, text=msg)
    # await bot.forward_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
