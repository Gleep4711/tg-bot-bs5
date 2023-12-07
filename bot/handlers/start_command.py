# from asyncio import sleep
from textwrap import dedent
# import re
# from random import randint

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

# from bot.const import START_POINTS, STICKER_FAIL, SPIN_TEXT, THROTTLE_TIME_SPIN
# from bot.dice_check import get_combo_data
from bot.keyboards import get_debug_keyboard, get_startsee_keyboard, get_home_keyboard
from bot.sql import users, connect
from bot.utilits import debug, log
from bot.const import START_WEAPON, START_ESCAPE, START_PARROT, \
                    STARTSEE_SEE, STARTSEE_ESCAPE, FISHERMAN, CAVE, \
                    STORAGE, DOCK, HOUSE, SHIPYARD, GROVE

flags = {"throttling_key": "default"}
router = Router()

@router.message(Text(text=[START_WEAPON, START_ESCAPE, START_PARROT]), flags=flags)
async def startcommand(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    if user['state'] != 'start': return await message.answer('Что-то пошло не так')

    answer_text = ''
    if message.text == START_WEAPON:
        answer_text = '''\
        Достав свою саблю ты вступаешь в неравную схватку с туманом. Ты пронзаешь насквозь выходящего из тумана 💀 скелета (?!) и он проделывает такую же процедуру с тобой...
        '''
        # Вы достаёте свою саблю и пронзаете первое что выходит из тумана, ваша сабля проходит насквозь скелета и скелет повторяет такую же процедуру с вами...
        debug('{} погиб с честью'.format(user['name']))
    elif message.text == START_ESCAPE:
        answer_text = '''\
        Вы сбежали с 🏝 острова. А, нет, показалось, коробль уже на дне, бежать некуда.
        '''
        debug('{} сбежал'.format(user['name']))
    elif message.text == START_PARROT:
        answer_text = '''\
        У вас не настолько холодное ❤️ сердце, чтобы принести в жертву своего верного помощника.
        '''
        debug('{} убил попугая'.format(user['name']))
    answer_text += '''\
        
        Ваше сердце пронзает ржавая сабля, вас окутывает чёрный туман, вы чувствуете как уходит жизнь...
        
        Проходит некоторое время, вы понимате что всё ещё чувствуете боль и кажется вы забыли что-то очень важное из своего детства.
        Вы с трудом открываете глаза, кажется ваши глаза не очень любят солёную воду и песок...
        '''
    conn = connect()
    conn.execute(users.update().values(state='startsee').where(users.c.user_id==message.from_user.id))
    conn.close()
    user['state'] = 'startsee'
    await state.update_data(user=user)
    
    await message.answer(dedent(answer_text), reply_markup=get_startsee_keyboard())

@router.message(Text(text=STARTSEE_SEE), flags=flags)
async def start_see(message: Message, state: FSMContext):

    user_data = await state.get_data()
    user = user_data.get('user')
    if user['location'] != 'start': return await message.answer('Что-то пошло не так')

    see_text = '''\
        Вы осматриваетесь вокруг:
        вы находитесь на маленьком 🏝островке, на котором много песка и пальм,
        на берегу вы видите рыбака, рядом с ним пришфартована 🛶маленькая лодка,
        кажется рыбак тут хранит большой запас 🍺рома, вы не можете оценить на сколько глубокая эта яма, но вы целиком уверены что она доверху заполнена бутылками с 🍺🍺🍺ромом,
        с другой стороны вы выдите разрушенные временем постройки, кажется тут были когда-то верфь с причалом, их легко будет ⚒восстановить,
        рядом с ними есть несколько 🛖лачуг, в них ещё можно жить, но судя по внешнему виду они давно пустуют,
        в роще вы видите много 🐵обезьян с 🦜попугаями и что-то похожее на вход в пещеру.
    '''
    if user['state'] == 'startsee':
        keyboard = get_startsee_keyboard()
    else:
        keyboard = get_home_keyboard()
    await message.answer(dedent(see_text), reply_markup=keyboard)

@router.message(Text(text=STARTSEE_ESCAPE), flags=flags)
async def start_run(message: Message, state: FSMContext):

    user_data = await state.get_data()
    user = user_data.get('user')
    conn = connect()
    conn.execute(users.update().values(state='home', location='home').where(users.c.user_id==message.from_user.id))
    conn.close()
    user['state'] = 'home'
    await state.update_data(user=user)

    see_text = '''\
        Вы всё ещё не понимаете где вы и что происходит...
        Вы бежите к лодке рыбака, отвязываете её и начинаете гребсти прочь от этого проклятого острова. 
        Через 20 метров вы замечате под поверхностью воды острые камни, но уже слишком поздно, камни прорезают лодку словно масло, забирая на дно лодку вместе с вами.
        На этот раз вы чувствуете как черный туман исходит прямо из вас и снова эта ужасная боль....
        
        Спустя какое то время, вы понимате что лежите на песке и если открыть глаза, то ничего хорошего не будет, но продолжать терпеть боль нет смысла.
        Рядом слышно шарканье по песку, открыв глаза вы видите рыбака протягивающего вам бутылку рома.
            — Первый раз умираешь? 
            Вот, держи, это утолит немного боль. 
            Боги что прислали нас сюда, не оставят нас в покое, им что-то от нас нужно. 
            С каждой смертью ты будешь просыпаться на своём острове, но с каждым разом будешь забывать немного о себе, о том, кто ты есть.
            Вот, возьми ещё карту, без неё здесь никуда. На карте отмечены ближайшие острова и безопасные пути до них.
    '''
    await message.answer(dedent(see_text), reply_markup=get_home_keyboard())

@router.message(Text(text=FISHERMAN), flags=flags)
async def fisherman(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    if user['location'] != 'home': return await message.answer('Что-то пошло не так')
    fisherman_text = '''\
        Я без труда могу построить рыбацкую лодку, благо дерева тут предостаточно. 
        Однако если ты хочешь корыто попрочнее, то придёться отремонтировать верфь.
        Я хорош в строительстве, но сам не справлюсь. Приведи мне пару работников.
        
        Золота у тебя нет, а аборигены за бесплатно работать не станут.
        В пещере можно найти какой нибудь ржавый меч, а в рыбацкой гавани есть рыбаки.
        Думаю ты что нибудь придумаешь.
        '''
    await message.answer(dedent(fisherman_text))

@router.message(Text(text=CAVE), flags=flags)
async def cave(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    if user['location'] != 'home': return await message.answer('Что-то пошло не так')
    await message.answer('Куда ты собрался в таком состоянии? Иди немного отдохнуть и приходи позже.')

@router.message(Text(text=STORAGE), flags=flags)
async def cave(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    if user['location'] != 'home': return await message.answer('Что-то пошло не так')
    storage_text = 'Яма выглядит достаточно глубокой чтобы положить в неё целый корабль, но пока она доверху заполнена 🍺 ромом. Вам придёться опустошить сотню - другую бутылок, прежде чем положить сюда хоть что-то.'
    storage = '''\
        🍺 Ром - ♾
        💰 Самолы - 0
        '''
        # Динар, малот, самол, лорик
    await message.answer('{}\n\nВ хранилище:\n{}'.format(storage_text, dedent(storage)))

@router.message(Text(text=DOCK), flags=flags)
async def cave(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    if user['location'] != 'home': return await message.answer('Что-то пошло не так')
    await message.answer('Куда ты собрался в таком состоянии? Иди немного отдохнуть и приходи позже.')

@router.message(Text(text=HOUSE), flags=flags)
async def cave(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    if user['location'] != 'home': return await message.answer('Что-то пошло не так')
    await message.answer('В разработке')

@router.message(Text(text=SHIPYARD), flags=flags)
async def cave(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    if user['location'] != 'home': return await message.answer('Что-то пошло не так')
    await message.answer('Ты смотришь на разрушенную верфь, сам тут не справишься, надо по меньшей мере ещё два работника для её восстановления.')

@router.message(Text(text=GROVE), flags=flags)
async def cave(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user = user_data.get('user')
    if user['location'] != 'home': return await message.answer('Что-то пошло не так')
    await message.answer('🐵 обезьяны закидывают тебя кокосами не позволяя подойти даже близко к пальмам...')
