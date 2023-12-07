from aiogram.filters.callback_data import CallbackData

class BastionInlineDynamic(CallbackData, prefix='bs'):
    data: str

