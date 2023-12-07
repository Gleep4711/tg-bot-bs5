from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

flags = {"throttling_key": "default"}
router = Router()


@router.message(Command('start'), flags=flags)
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("<b>Welcome</b>")


@router.message(Command('stop'), flags=flags)
async def cmd_stop(message: Message):
    await message.answer(
        "Клавиатура удалена. Начать заново: /start, вернуть клавиатуру и продолжить: /spin",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command('help'), flags=flags)
async def cmd_help(message: Message):
    help_text = \
        "В казино доступно 4 элемента: BAR, виноград, лимон и цифра семь. Комбинаций, соответственно, 64. " \
        "Для распознавания комбинации используется четверичная система, а пример кода " \
        "для получения комбинации по значению от Bot API можно увидеть " \
        "<a href='https://gist.github.com/MasterGroosha/963c0a82df348419788065ab229094ac'>здесь</a>.\n\n" \
        "Исходный код бота доступен на <a href='https://github.com/MasterGroosha/telegram-casino-bot'>GitHub</a> " \
        "и на <a href='https://git.groosha.space/shared/telegram-casino-bot'>GitLab</a>."
    await message.answer(help_text, disable_web_page_preview=True)


@router.message(Command('chat_info'), flags=flags)
async def chat_info(message: Message):
    msg = '''
    ID: <code>{}</code>
    topic id: <code>{}</code>
    type: {}
    title: {}
    username: {}
    invite_link: {}
    '''.format(
        message.chat.id,
        message.message_thread_id,
        message.chat.type,
        message.chat.title,
        message.chat.username,
        message.chat.invite_link,
    )

    await message.answer(msg or 'error')
