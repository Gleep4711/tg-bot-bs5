from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from bot.common import BastionInlineDynamic


def build_keyboard(data):
    keyboard = []
    for buttons in data:
        step = []
        for text_button in buttons:
            step.append(KeyboardButton(text=text_button))
        keyboard.append(step)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def build_inline(data) -> InlineKeyboardMarkup:
    kb = []
    for buttons in data:
        step = []
        for button in buttons:
            new_button = InlineKeyboardButton(
                text=button['text'],
                callback_data=BastionInlineDynamic(data='{}'.format(button['callback_data'])).pack(),
            )
            step.append(new_button)
        kb.append(step)
    return InlineKeyboardMarkup(inline_keyboard=kb)
