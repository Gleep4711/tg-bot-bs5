from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from bot.config_reader import config

if config.fsm_mode == 'redis':
    storage = RedisStorage.from_url(
        url=str(config.redis),
        connection_kwargs={'decode_responses': True}
    )
else:
    storage = MemoryStorage()

bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
dp = Dispatcher(storage=storage)
