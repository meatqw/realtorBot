from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import config
from db import db, Users, Objects, AccessKeys, app
from aiogram.types import ParseMode
from aiogram.utils.markdown import link
import logging
import aiogram.utils.markdown as md
import datetime
from yandex import get_data

KEYS = ['key']
OBJECTS = {}
FILTER = {}
USER = {}
UPDATE = {}
SWITCH = {}
NOTIFICATION = {}

def get_keys():
    # with app.app_context():
    #     return [i.key for i in AccessKeys.query.all()]
    return ['key']

logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# form userForm
class userForm(StatesGroup):
    fullname = State()
    phone = State()
    experience = State()
    job = State()
    key = State()
    region = State()
    city = State()

# form objectsForm


class objectsForm(StatesGroup):
    region = State()
    city = State()
    area = State()
    address = State()
    property_type = State()
    # street = State()
    rooms = State()
    stage = State()
    description = State()
    price = State()
    quadrature = State()
    number_of_storeys = State()
    phone = State()


# user data
class UserData(StatesGroup):
    current_price = State()
    
class Notification(StatesGroup):
    data = State()

class updateData(StatesGroup):
    data = State()

# ########################### REGISTRATION ###########################


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """START HANDLING"""

    # start fullname state
    await userForm.fullname.set()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['start_registration'])
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['enter_fullname'])


@dp.message_handler(state=userForm.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    """FULLNAME STATE"""

    async with state.proxy() as data:
        data['fullname'] = message.text

    # start phone state
    await userForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['enter_phone'])


@dp.message_handler(state=userForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    """PHONE STATE"""

    async with state.proxy() as data:
        data['phone'] = message.text

    # start expirience state
    await userForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['enter_experience'])


@dp.message_handler(state=userForm.experience)
async def process_experience(message: types.Message, state: FSMContext):
    """EXPERIENCE STATE"""

    async with state.proxy() as data:
        data['experience'] = message.text

    # start job state
    await userForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['enter_job'])


@dp.message_handler(state=userForm.job)
async def process_job(message: types.Message, state: FSMContext):
    """JOB STATE"""

    async with state.proxy() as data:
        data['job'] = message.text

    # start key state
    await userForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['enter_key'])


@dp.message_handler(lambda message: message.text not in get_keys(), state=userForm.key)
async def process_check_key(message: types.Message):
    """CHECK KEY"""
    return await message.reply(config.OBJECT_TEXT['user']['exc_key'])


@dp.message_handler(lambda message: message.text in get_keys(), state=userForm.key)
async def process_key(message: types.Message, state: FSMContext):
    """KEY STATE"""

    # start region state
    await userForm.next()
    # update key in state
    await state.update_data(key=message.text)
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['enter_region'])


@dp.message_handler(lambda message: len(message.text) < 0, state=userForm.region)
async def process_user_region_invalid(message: types.Message):
    return await message.reply(config.OBJECT_TEXT['user']['exc_region'])


@dp.message_handler(lambda message: len(message.text) > 0, state=userForm.region)
async def process_user_region(message: types.Message, state: FSMContext):
    """USER REGION STATE"""

    async with state.proxy() as data:
        data['region'] = message.text

    # start objects city state
    await userForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['enter_city'])


@dp.message_handler(lambda message: len(message.text) < 0, state=userForm.city)
async def process_user_city_invalid(message: types.Message):
    return await message.reply(config.OBJECT_TEXT['user']['exc_city'])


@dp.message_handler(lambda message: len(message.text) > 0, state=userForm.city)
async def process_city(message: types.Message, state: FSMContext):
    """USER CITY STATE"""

    msg = await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['loading'])

    async with state.proxy() as data:
        city = get_data(f"{data['region']}, {message.text}", "region_city")
        data['city'] = city['city']
        data['region'] = city['region']
        
        try:
            login = message.chat.username
        except Exception as e:
            login = '-'

        with app.app_context():
        # save USER data in db
            user = Users(
                id=str(message.chat.id),
                login=login,
                fullname=data['fullname'],
                phone=data['phone'],
                experience=data['experience'],
                job=data['job'],
                key=data['key'],
                region=data['region'],
                city=data['city'],
                notification={'status': False, 'filter': None})

            db.session.add(user)
            db.session.commit()

        await msg.delete()

        # send user data
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(config.OBJECT_TEXT['user']['finish_registration']),
                md.text('ФИО: ', md.bold(data['fullname'])),
                md.text('Номер: ', md.bold(data['phone'])),
                md.text('Стаж: ', md.bold(data['experience'])),
                md.text('Место работы: ', md.bold(data['job'])),
                md.text('Ключ: ', md.bold(data['key'])),
                md.text('Регион: ', md.bold(data['region'])),
                md.text('Город: ', md.bold(data['city'])),
                md.text(
                    md.bold(config.OBJECT_TEXT['user']['finish_reg_text'])),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
        # with app.app_context():
        #     access_key = AccessKeys.query.filter_by(key=data['key']).first()
        #     access_key.user = str(message.chat.id)
        #     db.session.commit()

    # finish state
    await state.finish()

# CHECK AUTH USER

# main keyboard
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.row(
    config.OBJECT_TEXT['main']['sale_btn'], config.OBJECT_TEXT['main']['feed_btn'])
main_keyboard.row(config.OBJECT_TEXT['main']['my_objects_btn'],
                  config.OBJECT_TEXT['main']['notification_btn'])

def get_user_(id):
    with app.app_context():
        return Users.query.filter_by(id=id).first()


@dp.message_handler(lambda message: get_user_(message.chat.id) != None
                    and message.text not in [config.OBJECT_TEXT['main'][i] for i in config.OBJECT_TEXT['main']] and 
                    message.text not in [config.OBJECT_TEXT['notification'][i] for i in config.OBJECT_TEXT['notification']])
async def process_auth(message: types.Message):
    """USER AUTH"""

    await message.answer(config.OBJECT_TEXT['user']['login'], reply_markup=main_keyboard)


@dp.message_handler(lambda message: get_user_(message.chat.id) == None
                    and message.text not in [config.OBJECT_TEXT['main'][i] for i in config.OBJECT_TEXT['main']] and 
                    message.text not in [config.OBJECT_TEXT['notification'][i] for i in config.OBJECT_TEXT['notification']])
async def process_not_auth(message: types.Message):
    """USER NOT AUTH"""
    markup = types.ReplyKeyboardRemove()

    await bot.send_message(
        message.chat.id, config.OBJECT_TEXT['user']['not_login'],
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


# ####################### FUNCTIONS #################################

@dp.message_handler(Text(equals=config.OBJECT_TEXT['main']['cancel_btn'], ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """CANCEL HANDLER"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['main']['cancel_ok'], reply_markup=main_keyboard)


@dp.message_handler(Text(equals=config.OBJECT_TEXT['main']['back_btn'], ignore_case=True), state='*')
async def back_handler(message: types.Message,  state: FSMContext):
    """BACK HANDLER"""

    await bot.send_message(message.chat.id, config.OBJECT_TEXT['main']['back_ok'], reply_markup=main_keyboard)

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

# ---------------------- SALE -----------------------

from sale import *

# -------------------- FEED -----------------------


@dp.message_handler(Text(equals=config.OBJECT_TEXT['main']['feed_btn']))
async def function_feed(message: types.Message):
    """FUNCTION FEED"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(config.OBJECT_TEXT['main']['back_btn'])

    await bot.send_message(message.chat.id, config.OBJECT_TEXT['feed']['feed'], reply_markup=keyboard)

    # filter switch
    filter_keyboard = types.InlineKeyboardMarkup(
        resize_keyboard=True, selective=True)

    filter_keyboard.add(*[
        types.InlineKeyboardButton(
            f'✅ Да', callback_data=f'filter_switch_yes'),
        types.InlineKeyboardButton(
            f'❌ Нет', callback_data=f'filter_switch_no')
    ])

    await bot.send_message(message.chat.id, config.OBJECT_TEXT['feed']['switch_filter'], reply_markup=filter_keyboard)

    OBJECTS[message.chat.id] = {}


def render_all_feed(obj):
    """FEED. RENDER ALL OBJECTS"""
    feed_keyboard = types.InlineKeyboardMarkup(
        resize_keyboard=True, selective=True, row_width=1)
    buttons = []
    for object in obj:
        buttons.append(types.InlineKeyboardButton(f'{object.city}, {object.address}, {object.price}',
                                                  callback_data=f'object_feed_{object.id}'))

    feed_keyboard.add(*buttons)
    return feed_keyboard


def render_filter_button(id):
    """FEED. RENDER FILTER BUTTONS"""
    filter_items_keyboard = types.InlineKeyboardMarkup(
        resize_keyboard=True, selective=True, row_width=1)

    if id in FILTER:
        with app.app_context():
            user = Users.query.filter_by(id=id).first()

        if 'region' in FILTER[id]:
            current_region = FILTER[id]['region']
        else:
            # user city
            current_region = user.region

        if 'city' in FILTER[id]:
            current_city = FILTER[id]['city']
        else:
            # user city
            current_city = 'Не выбрано'

        if 'area' in FILTER[id]:
            current_area = FILTER[id]['area']
        else:
            current_area = 'Не выбрано'

        if 'rooms' in FILTER[id]:
            current_rooms = FILTER[id]['rooms']
        else:
            current_rooms = 'Не выбрано'

        if 'price' in FILTER[id]:

            try:
                current_price = FILTER[id]['price']['text']
            except Exception as e:
                current_price = 'Не выбрано'
        else:
            current_price = 'Не выбрано'

        if 'count' in FILTER[id]:
            current_count = len(get_result_objects(id))
        else:
            with app.app_context():
                current_count = len(
                    Objects.query.filter_by(region=current_region).all())
    else:

        # default user city and region

        with app.app_context():
            user = Users.query.filter_by(id=id).first()
        current_region = user.region
        current_city = 'Не выбрано'
        current_area = 'Не выбрано'
        current_rooms = 'Не выбрано'
        current_price = 'Не выбрано'
        with app.app_context():
            current_count = len(Objects.query.filter_by(city=current_city).all())

        FILTER[id] = {'city': current_city, 'area': current_area,
                      'rooms': current_rooms, 'price': current_price,
                      'count': current_count, 'region': current_region}

    buttons = [
        types.InlineKeyboardButton(
            f"{config.OBJECT_TEXT['feed']['region_btn']}: {current_region}", callback_data='filter_item_region'),
        types.InlineKeyboardButton(
            f"{config.OBJECT_TEXT['feed']['city_btn']}: {current_city}", callback_data='filter_item_city'),
        types.InlineKeyboardButton(
            f"{config.OBJECT_TEXT['feed']['area_btn']}: {current_area}", callback_data='filter_item_area'),
        types.InlineKeyboardButton(
            f"{config.OBJECT_TEXT['feed']['rooms_btn']}: {current_rooms}", callback_data='filter_item_rooms'),
        types.InlineKeyboardButton(
            f"{config.OBJECT_TEXT['feed']['price']}: {current_price}", callback_data='filter_item_price')
    ]
    
    filter_items_keyboard.add(*buttons)
    if SWITCH[id]['current'] == 'objects':
        filter_items_keyboard.row(types.InlineKeyboardButton(
            f"{config.OBJECT_TEXT['feed']['feed_ok_filter']} ({current_count})", callback_data='filter_item_ok'), 
                                  types.InlineKeyboardButton(f"{config.OBJECT_TEXT['feed']['clear']}", callback_data='filter_item_clear'))
        
    else:
        filter_items_keyboard.row(types.InlineKeyboardButton(f"{config.OBJECT_TEXT['notification']['filter_btn_ok']}", callback_data='filter_notification_ok'))
    
    
    return filter_items_keyboard


async def render_item(id, item):
    """RENDER FILTER ITEM"""
    if 'current_item' in FILTER[id]:
        try:
            await FILTER[id]['current_item'].delete()
        except Exception as e:
            print(e)

    keyboard_items = types.InlineKeyboardMarkup(
        resize_keyboard=True, selective=True, row_width=1)

    # get all objects
    with app.app_context():
        objects = Objects.query.all()
    all_city = set([i.city for i in objects if i.city != None])
    all_areas_filter_by_city = set(
        [i.area for i in objects if i.city == FILTER[id]['city']])
    all_objects_rooms_filter_by_city = set(
        [i.rooms for i in objects if i.city == FILTER[id]['city']])

    all_region = set([i.region for i in objects])

    buttons = []

    # all refion
    if item == 'region':
        for i in all_region:
            buttons.append(types.InlineKeyboardButton(
                f'{i}', callback_data=f'filter_region_{i}'))

        keyboard_items.add(*buttons)

        msg = await bot.send_message(id, config.OBJECT_TEXT['feed']['region_btn'], reply_markup=keyboard_items)

    # all cities
    if item == 'city':
        for i in all_city:
            buttons.append(types.InlineKeyboardButton(
                f'{i}', callback_data=f'filter_city_{i}'))

        keyboard_items.add(*buttons)

        msg = await bot.send_message(id, config.OBJECT_TEXT['feed']['city_btn'], reply_markup=keyboard_items)

    # all areas by current city
    elif item == 'area':

        for i in all_areas_filter_by_city:
            buttons.append(types.InlineKeyboardButton(
                f'{i}', callback_data=f'filter_area_{i}'))

        keyboard_items.add(*buttons)

        msg = await bot.send_message(id, config.OBJECT_TEXT['feed']['area_btn'], reply_markup=keyboard_items)

    elif item == 'rooms':

        for i in all_objects_rooms_filter_by_city:
            buttons.append(types.InlineKeyboardButton(
                f'{i}', callback_data=f'filter_rooms_{i}'))

        keyboard_items.add(*buttons)

        msg = await bot.send_message(id, config.OBJECT_TEXT['feed']['rooms_btn'], reply_markup=keyboard_items)

    elif item == 'price':

        msg = await bot.send_message(id, config.OBJECT_TEXT['feed']['enter_current_price'])

        await UserData.current_price.set()

        # data to delete
        FILTER[id]['trash'] = [msg]

    FILTER[id]['current_item'] = msg

@dp.message_handler(lambda message: '-' not in message.text, state=UserData.current_price)
async def process_current_filter_price_invalid(message: types.Message):

    item = await message.reply(config.OBJECT_TEXT['feed']['exc_current_price'])

    # add in trash
    FILTER[message.chat.id]['trash'].append(item)
    FILTER[message.chat.id]['trash'].append(message)

    return item


@dp.message_handler(lambda message: '-' in message.text, state=UserData.current_price)
async def process_current_filter_price(message: types.Message, state: FSMContext):
    """CURRENT FILTER PRICE PROCESS"""

    # add in trash
    FILTER[message.chat.id]['trash'].append(message)

    async with state.proxy() as data:
        try:
            data['current_price'] = message.text.strip().replace(' ', '')
            FILTER[message.chat.id]['price'] = {'text': message.text.strip().replace(' ', ''),
                                        'min': data['current_price'].split('-')[0],
                                        'max': data['current_price'].split('-')[1]}
        except Exception as e:
            print(e)

    try:
        # clear trash
        for i in FILTER[message.chat.id]['trash']:
            await i.delete()
    except Exception as e:
        print(e)

    try:
        # delete current filter menu
        await FILTER[message.chat.id]['filter_menu'].delete()
    except Exception as e:
        print(e)

    filter_menu = await bot.send_message(message.chat.id, config.OBJECT_TEXT['feed']['filter'], reply_markup=render_filter_button(message.chat.id))
    FILTER[message.chat.id]['filter_menu'] = filter_menu

    # finish state
    await state.finish()


def get_result_objects(id):
    
    filter_region = FILTER[id]['region']
    filter_city = FILTER[id]['city']
    filter_area = FILTER[id]['area']
    filter_price = FILTER[id]['price']
    filter_rooms = FILTER[id]['rooms']

    res_objects = []

    # true true true
    if filter_area != 'Не выбрано' and filter_rooms != 'Не выбрано' and filter_city != 'Не выбрано':
        with app.app_context():
            objects = Objects.query.filter_by(
                region=filter_region, area=filter_area, rooms=filter_rooms, city=filter_city).all()

    # true false false
    elif filter_area != 'Не выбрано' and filter_rooms == 'Не выбрано' and filter_city == 'Не выбрано':
        with app.app_context():
            objects = Objects.query.filter_by(
                region=filter_region, area=filter_area).all()

    # false true false
    elif filter_area == 'Не выбрано' and filter_rooms != 'Не выбрано' and filter_city == 'Не выбрано':
        with app.app_context():
            objects = Objects.query.filter_by(
                region=filter_region, rooms=filter_rooms).all()

    # false false true
    elif filter_area == 'Не выбрано' and filter_rooms == 'Не выбрано' and filter_city != 'Не выбрано':
        with app.app_context():
            objects = Objects.query.filter_by(
                region=filter_region, city=filter_city).all()

    # true true false
    elif filter_area != 'Не выбрано' and filter_rooms != 'Не выбрано' and filter_city == 'Не выбрано':
        with app.app_context():
            objects = Objects.query.filter_by(
                region=filter_region, area=filter_area, rooms=filter_rooms).all()

    # true false true
    elif filter_area != 'Не выбрано' and filter_rooms == 'Не выбрано' and filter_city != 'Не выбрано':
        with app.app_context():
            objects = Objects.query.filter_by(
                region=filter_region, area=filter_area, city=filter_city).all()

    # false true true
    elif filter_area == 'Не выбрано' and filter_rooms != 'Не выбрано' and filter_city != 'Не выбрано':
        with app.app_context():
            objects = Objects.query.filter_by(
                region=filter_region, rooms=filter_rooms, city=filter_city).all()

    # false false false
    elif filter_area == 'Не выбрано' and filter_rooms == 'Не выбрано' and filter_city == 'Не выбрано':
        with app.app_context():
            objects = Objects.query.filter_by(region=filter_region).all()

    if filter_price != 'Не выбрано':
        for i in objects:
            if int(filter_price['max']) >= int(i.price) >= int(filter_price['min']):
                res_objects.append(i)
    else:
        res_objects = objects

    return res_objects

async def set_item_filter_notification(id, item):
    """ENTER VALUE FOR NOTIFICATION FILTER"""
    msg = await bot.send_message(id, config.OBJECT_TEXT['notification']['enter_value'])
    
    NOTIFICATION[id]['current_filter_item'] = item
    NOTIFICATION[id]['current_filter_msg'] = msg
    await Notification.data.set()
    
@dp.message_handler(lambda message: len(message.text) > 0, state=Notification.data)
async def process_value_notification(message: types.Message, state: FSMContext):
    """VALUE FOR NOTIFICATION PROCESS"""

    async with state.proxy() as data:
        item = NOTIFICATION[message.chat.id]['current_filter_item']
        
        if item == 'city':
            valid_data = get_data(f'{FILTER[message.chat.id]["region"]}, {message.text}', 'region_city')
            FILTER[message.chat.id][item] = valid_data['city']
        else:
            FILTER[message.chat.id][item] = message.text
            
        NOTIFICATION[message.chat.id]['user_msg'] = message

    # finish state
    await state.finish()
    
    # delete trash
    await NOTIFICATION[message.chat.id]['user_msg'].delete()
    await NOTIFICATION[message.chat.id]['current_filter_msg'].delete()
    
    try:
        # delete old filter menu
        await FILTER[message.chat.id]['filter_menu'].delete()
    except Exception as e:
        print(e)
        
    filter_menu = await bot.send_message(message.chat.id, config.OBJECT_TEXT['feed']['filter'], reply_markup=render_filter_button(message.chat.id))
    
    FILTER[message.chat.id]['filter_menu'] = filter_menu
    
    

@dp.callback_query_handler(Text(startswith="filter_"))
async def callback_filter(call: types.CallbackQuery):
    """CALLBACK FILTER"""

    action = call.data.split('_')[-1]
    func_action = call.data.split('_')[-2]

    try:
        await OBJECTS[call.message.chat.id]['current_object'].delete()
    except Exception as e:
        pass

    try:
        for i in FILTER[call.message.chat.id]['objects']:
            await i.delete()
    except Exception as e:
            print(e)

    # switch yes/no
    if func_action == 'switch':
        if action == 'yes':
            # toggle filter application
            SWITCH[call.message.chat.id] = {'current': 'objects'}
            
            filter_menu = await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['feed']['filter'], reply_markup=render_filter_button(call.message.chat.id))
            FILTER[call.message.chat.id]['filter_menu'] = filter_menu
            
        elif action == 'no':
            # get objects without filter
            with app.app_context():
                object = Objects.query.all()
            
            for i in render_all_objects(object):
                await bot.send_message(call.message.chat.id, i[0], parse_mode=ParseMode.MARKDOWN)

    # filter items
    elif func_action == 'item':
    
        if action == 'region':
            
            await render_item(call.message.chat.id, 'region')
            
        elif action == 'city':
            
            # FEED MODE
            if SWITCH[call.message.chat.id]['current'] == 'objects':
                await render_item(call.message.chat.id, 'city')
            else:
                await set_item_filter_notification(call.message.chat.id, 'city')
            
            
        elif action == 'area':
            
            # FEED MODE
            if SWITCH[call.message.chat.id]['current'] == 'objects':
                await render_item(call.message.chat.id, 'area')
            else:
                await set_item_filter_notification(call.message.chat.id, 'area')
            
        elif action == 'rooms':
            
            # FEED MODE
            if SWITCH[call.message.chat.id]['current'] == 'objects':
                await render_item(call.message.chat.id, 'rooms')
            else:
                await set_item_filter_notification(call.message.chat.id, 'rooms')
                
        elif action == 'price':
            await render_item(call.message.chat.id, 'price')
            
        elif action == 'ok':
           
            res_objects = get_result_objects(call.message.chat.id)
            if len(res_objects) > 0:
                # render objects 
                # objects_btn = await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['feed']['objects_with_filter'], reply_markup=render_all_feed(res_objects))
                FILTER[call.message.chat.id]['objects'] = []
                for i in render_all_objects(res_objects):
                    msg = await bot.send_message(call.message.chat.id, i[0], parse_mode=ParseMode.MARKDOWN)
                    
                    FILTER[call.message.chat.id]['objects'].append(msg)
            else:
                objects_btn = await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['feed']['no_objects'])
                FILTER[call.message.chat.id]['objects_btn'] = objects_btn 
                
        # clear filter
        elif action == 'clear':
            FILTER[call.message.chat.id]['region'] = 'Не выбрано' 
            FILTER[call.message.chat.id]['area'] = 'Не выбрано' 
            FILTER[call.message.chat.id]['rooms'] = 'Не выбрано' 
            FILTER[call.message.chat.id]['price'] = 'Не выбрано' 
            FILTER[call.message.chat.id]['city'] = 'Не выбрано' 
            
            try:
                # delete old filter menu
                await FILTER[call.message.chat.id]['filter_menu'].delete()
            except Exception as e:
                print(e)
            
            try:
                for i in FILTER[call.message.chat.id]['objects']:
                    await i.delete()
            except Exception as e:
                print(e)
            
            try:
                # delete buttons
                await FILTER[call.message.chat.id]['current_item'].delete()
            except Exception as e:
                print(e)
                
            
                
            filter_menu = await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['feed']['filter'], reply_markup=render_filter_button(call.message.chat.id))
            
            FILTER[call.message.chat.id]['filter_menu'] = filter_menu
            
    # notification filter OK
    elif func_action == 'notification':
        with app.app_context():
            user = Users.query.filter_by(id=call.message.chat.id).first()
        
        try:
            await FILTER[call.message.chat.id]['filter_menu'].delete()
        except Exception as e:
            print(e)
        
        try:
            del FILTER[call.message.chat.id]['filter_menu']
        except Exception as e:
            print(e)
        
        try:
            for i in FILTER[call.message.chat.id]['objects']:
                await i.delete()
                del FILTER[call.message.chat.id]['objects']
        except Exception as e:
            print(e)
        
        try:
            del FILTER[call.message.chat.id]['objects']
        except Exception as e:
            print(e)
        
        try:
            # delete buttons
            await FILTER[call.message.chat.id]['current_item'].delete()
        except Exception as e:
            print(e)
        
        try:
            del FILTER[call.message.chat.id]['current_item']
        except Exception as e:
            print(e)
        
        try:
            await FILTER[call.message.chat.id]['trash'].delete()
        except Exception as e:
            print(e)
        
        try:
            del FILTER[call.message.chat.id]['trash']
        except Exception as e:
            print(e)
        
        
        print(FILTER[call.message.chat.id])
        user.notification = {'status': True, 'filter': FILTER[call.message.chat.id]}
        db.session.commit()
        
        await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['notification']['filter_ok'])
            
    else:
        # if the city is changes, area and rooms is cleared
        
        if func_action == 'city':
            FILTER[call.message.chat.id]['area'] = 'Не выбрано' 
            FILTER[call.message.chat.id]['rooms'] = 'Не выбрано' 
            FILTER[call.message.chat.id]['price'] = 'Не выбрано'
        elif func_action == 'region':
            FILTER[call.message.chat.id]['area'] = 'Не выбрано' 
            FILTER[call.message.chat.id]['rooms'] = 'Не выбрано' 
            FILTER[call.message.chat.id]['price'] = 'Не выбрано'
            FILTER[call.message.chat.id]['city'] = 'Не выбрано'
            
            
        FILTER[call.message.chat.id][func_action] = action
        
        try:
            for i in FILTER[call.message.chat.id]['objects']:
                await i.delete()
        except Exception as e:
                print(e)
        
        try:
            # delete buttons
            await FILTER[call.message.chat.id]['current_item'].delete()
        except Exception as e:
            print(e)
            
        try:
            # delete old filter menu
            await FILTER[call.message.chat.id]['filter_menu'].delete()
        except Exception as e:
            print(e)
            
        filter_menu = await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['feed']['filter'], reply_markup=render_filter_button(call.message.chat.id))
        
        FILTER[call.message.chat.id]['filter_menu'] = filter_menu
    

# -------------------- MY OBJECTS ------------------------

def price_processing(price):
    
    arr = ([price[::-1][i:i + 3] for i in range(0, len(price[::-1]), 3)])
    arr = list(reversed(arr))
    price = '.'.join(arr)
    return price
    

def render_all_objects(my_objects):
    """RENDER ALL MY OBJECTS"""
    
    objects = []
    for object in reversed(my_objects):
        
        object_control_keyboard = types.InlineKeyboardMarkup(
        resize_keyboard=True, selective=True)
    
        object_control_keyboard.add(*[
            types.InlineKeyboardButton(
                f'⏱ Продлить', callback_data=f'extend_object_{object.id}'),
            types.InlineKeyboardButton(
                f'🔄 Изменить', callback_data=f'update_object_{object.id}'),
            types.InlineKeyboardButton(
                f'🗑 Удалить', callback_data=f'del_object_{object.id}')
            
        ])

        text = md.text(
            md.text('Регион: ', md.bold(object.region)),
            md.text('Город: ', md.bold(object.city)),
            md.text('Район: ', md.bold(object.area)),
            md.text('Адрес: ', md.bold(object.address)),
            # md.text('Улица: ', md.bold(object.street)),
            md.text('Кол-во комнат: ', md.bold(object.rooms)),
            md.text('Этаж: ', md.bold(object.stage)),
            md.text('Описание: ', md.bold(object.description)),
            md.text('Цена: ', price_processing(str(object.price)) + ' ₽'),
            md.text('Площадь: ', str(object.quadrature) + ' м²'),
            md.text('Тип недвижимости: ', md.bold(object.property_type)),
            md.text('Этажность: ', md.bold(object.number_of_storeys)),
            md.text('Телефон: ', (f"[{object.phone}](tel:{object.phone})")),
            md.text('Дейтвительно до: ', (object.date_end.strftime("%d.%m.%Y, %H:%M:%S"))),

            sep='\n',
        )
        
        objects.append([text, object_control_keyboard])
    
    return objects
        

@dp.message_handler(Text(equals=config.OBJECT_TEXT['main']['my_objects_btn']))
async def function_my_objects(message: types.Message):
    """FUNCTION MY OBJECTS"""
    id = message.chat.id
    with app.app_context():
        object = Objects.query.filter_by(user=id).all()
    
    OBJECTS[id] = {'msg': []}
    for i in render_all_objects(object):
        msg = await bot.send_message(id, i[0], reply_markup=i[1], parse_mode=ParseMode.MARKDOWN)
        OBJECTS[id]['msg'].append(msg)

# def render_my_object_info(object):
#     # add buttons
    
    
    
# @dp.callback_query_handler(Text(startswith="object_"))
# async def callbacks_my_object(call: types.CallbackQuery):
#     """CALLBACK MY OBJECT/FEED"""
#     action = call.data.split('_')[-1]
#     func_action = call.data.split('_')[-2]

#     # get data from db MY OBJECTS/FEED
#     object = Objects.query.filter_by(id=int(action)).first()

#     object_control_keyboard, text = render_my_object_info(object)

#     if 'current_object' in OBJECTS[call.message.chat.id]:
#         try:
#             await OBJECTS[call.message.chat.id]['current_object'].delete()
#         except Exception as e:
#             print(e)


#     if func_action == 'my':
#         # send object data (MY OBJECTS)
#         message_object_id = await bot.send_message(
#             call.message.chat.id,
#             text,
#             reply_markup=object_control_keyboard,
#             parse_mode=ParseMode.MARKDOWN,
#         )
#     else:
#         # send object data FEED
#         message_object_id = await bot.send_message(
#             call.message.chat.id,
#             text,
#             parse_mode=ParseMode.MARKDOWN,
#         )

#     # save current object
#     OBJECTS[call.message.chat.id]['current_object'] = message_object_id


@dp.callback_query_handler(Text(startswith="del_object_"))
async def callback_delete_my_object(call: types.CallbackQuery):
    """CALLBACK DELETE OBJECT"""
    action = call.data.split('_')[-1]

    try:
        await OBJECTS[call.message.chat.id]['current_object'].delete()
    except Exception as e:
        pass
    
    try:
        # del rec DB
        with app.app_context():
            Objects.query.filter_by(id=int(action)).delete()
            db.session.commit()
    except Exception as e:
        print(e)

    # rerender my object form
    try:
        for i in OBJECTS[call.message.chat.id]['msg']:
            await i.delete()
        del OBJECTS[call.message.chat.id]['msg']
    except Exception as e:
        pass

    try:
        for i in OBJECTS[call.message.chat.id]['object_list']:
            await i.delete()
        del OBJECTS[call.message.chat.id]['object_list']
    except Exception as e:
        pass
    
    with app.app_context():
        object = Objects.query.filter_by(user=call.message.chat.id).all()
        objects = render_all_objects(object)

    msgs = []
    for i in objects:
        msg = await bot.send_message(call.message.chat.id, i[0], reply_markup=i[1], parse_mode=ParseMode.MARKDOWN)
        msgs.append(msg)

    # save current object list
    OBJECTS[call.message.chat.id] = {'object_list': msgs}


@dp.callback_query_handler(Text(startswith="extend_object_"))
async def callback_extend_my_object(call: types.CallbackQuery):
    """CALLBACK EXTEND OBJECT"""
    action = call.data.split('_')[-1]

    try:
        await OBJECTS[call.message.chat.id]['current_object'].delete()
    except Exception as e:
        pass

    # update rec DB
    with app.app_context():
        object = Objects.query.filter_by(id=int(action)).first()
        object.date_end += datetime.timedelta(days=30)
        db.session.commit()

    try:
        del OBJECTS[call.message.chat.id]['current_object']
    except Exception as e:
        pass

@dp.callback_query_handler(Text(startswith="update_object_"))
async def callback_update_my_object(call: types.CallbackQuery):
    """CALLBACK UPDATE OBJECT"""
    id = call.data.split('_')[-1]
    
    # update menu
    update_keyboard = types.InlineKeyboardMarkup(
        resize_keyboard=True, selective=True)

    update_keyboard.add(*[
        types.InlineKeyboardButton(
            f'Регион', callback_data=f'update_region_{id}'),
        types.InlineKeyboardButton(
            f'Город', callback_data=f'update_city_{id}'),
        types.InlineKeyboardButton(
            f'Район', callback_data=f'update_area_{id}'),
        types.InlineKeyboardButton(
            f'Адрес', callback_data=f'update_address_{id}'),
        types.InlineKeyboardButton(
            f'Кол-во комнат', callback_data=f'update_rooms_{id}'),
        types.InlineKeyboardButton(
            f'Этаж', callback_data=f'update_stage_{id}'),
        types.InlineKeyboardButton(
            f'Описание', callback_data=f'update_description_{id}'),
        types.InlineKeyboardButton(
            f'Площадь', callback_data=f'update_quadrature_{id}'),
        types.InlineKeyboardButton(
            f'Тип недвижимости', callback_data=f'update_property_type_{id}'),
        types.InlineKeyboardButton(
            f'Этажность', callback_data=f'update_number_of_storeys_{id}'),
        types.InlineKeyboardButton(
            f'Телефон', callback_data=f'update_phone_{id}'),
        types.InlineKeyboardButton(
            f'Цена', callback_data=f'update_price_{id}'),
        types.InlineKeyboardButton(
            f'Отмена', callback_data=f'update_cancel_{id}'),
    ])

    msg = await bot.send_message(call.message.chat.id, "Выберите пункт для обновления", reply_markup=update_keyboard)
    UPDATE[call.message.chat.id] = {'trash': msg}
    
@dp.callback_query_handler(Text(startswith="update_"))
async def callbacks_update(call: types.CallbackQuery):
    """CALLBACK UPDATE"""
    id = call.data.split('_')[-1]
    action = call.data.split('update_')[1].replace(f'_{id}', '')
    UPDATE[call.message.chat.id]['update'] = {'action': action, 'id': id}
    
    await bot.send_message(call.message.chat.id, "Введите новое значение")
    await updateData.data.set()

@dp.message_handler(state=updateData.data)
async def process_update(message: types.Message, state: FSMContext):
    """UPDATE PROCESS"""
    
    try:
        await OBJECTS[message.chat.id]['current_object'].delete()
    except Exception as e:
        print(e)
    
    try:
        await UPDATE[message.chat.id]['trash'].delete()
    except Exception as e:
        print(e)
    
    async with state.proxy() as data: 
        # update data in db
        
        action = UPDATE[message.chat.id]['update']['action']
        id = UPDATE[message.chat.id]['update']['id']
        # SQL
        with app.app_context():
            db.engine.execute(f"UPDATE objects SET {action}={message.text} WHERE id={id};")
            db.session.commit()


    # finish state
    await state.finish()
    
    # reload object info
    with app.app_context():
        object = Objects.query.filter_by(id=UPDATE[message.chat.id]['update']['id']).all()
    text, object_control_keyboard  = render_all_objects(object)[0]
    
    message_object_id = await bot.send_message(
            message.chat.id,
            text,
            reply_markup=object_control_keyboard,
            parse_mode=ParseMode.MARKDOWN,
        )
    # save current object
    
    OBJECTS[message.chat.id]['current_object'] = message_object_id


@dp.message_handler(Text(equals=config.OBJECT_TEXT['main']['notification_btn']))
async def function_notifications(message: types.Message):
    """FUNCTION NOTIFICATIONS"""

    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(config.OBJECT_TEXT['notification']['yes'], config.OBJECT_TEXT['notification']['no'])
    keyboard.add(config.OBJECT_TEXT['notification']['filter'], config.OBJECT_TEXT['notification']['all'])
    keyboard.add(config.OBJECT_TEXT['main']['back_btn'])
    
    # printing current notification status
    with app.app_context():
        user_settings = Users.query.filter_by(id=message.chat.id).first()
    status = user_settings.notification['status']
    
    if status == False:
        status = '🔕'
    elif status == True:
        status = '🔔'
    await bot.send_message(message.chat.id, f"{config.OBJECT_TEXT['notification']['settings']} ({status})", reply_markup=keyboard)
    
@dp.message_handler(Text(equals=config.OBJECT_TEXT['notification']['yes'], ignore_case=True), state='*')
async def notification_yes_handler(message: types.Message,  state: FSMContext):
    """NOTIFICATON YES HANDLER"""

    with app.app_context():
        user_settings = Users.query.filter_by(id=message.chat.id).first()
        user_settings.notification = {'status': True, 'filter': None}
        db.session.commit()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['notification']['yes'], reply_markup=main_keyboard)

@dp.message_handler(Text(equals=config.OBJECT_TEXT['notification']['no'], ignore_case=True), state='*')
async def notification_no_handler(message: types.Message,  state: FSMContext):
    """NOTIFICATON NO HANDLER"""

    with app.app_context():
        user_settings = Users.query.filter_by(id=message.chat.id).first()
        user_settings.notification = {'status': False, 'filter': None}
        db.session.commit()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['notification']['no'], reply_markup=main_keyboard)

@dp.message_handler(Text(equals=config.OBJECT_TEXT['notification']['all'], ignore_case=True), state='*')
async def notification_all_handler(message: types.Message,  state: FSMContext):
    """NOTIFICATON ALL HANDLER"""

    with app.app_context():
        user_settings = Users.query.filter_by(id=message.chat.id).first()
        user_settings.notification = {'status': True, 'filter': None}
        db.session.commit()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['notification']['all'], reply_markup=main_keyboard)


@dp.message_handler(Text(equals=config.OBJECT_TEXT['notification']['filter'], ignore_case=True), state='*')
async def notification_filter_handler(message: types.Message,  state: FSMContext):
    """NOTIFICATON FILTER HANDLER"""
    
    # toggle filter application
    SWITCH[message.chat.id] = {'current': 'notification'}
    # user_settings = Users.query.filter_by(id=message.chat.id).first()
    
    # user init in NOTIFICATION DICT
    NOTIFICATION[message.chat.id] = {}
    
    
    msg = await bot.send_message(message.chat.id, config.OBJECT_TEXT['notification']['filter'], reply_markup=render_filter_button(message.chat.id))
    FILTER[message.chat.id]['filter_menu'] = msg

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
