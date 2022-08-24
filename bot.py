from distutils import extension
from distutils.errors import DistutilsFileError
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import config
from db import db, Users, Objects
from aiogram.types import ParseMode
import logging
import aiogram.utils.markdown as md

KEYS = ['key']


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
    
# form objectsForm
class objectsForm(StatesGroup):
    region = State()
    city = State()
    address = State()
    street = State()
    stage = State()
    description = State()
    price = State()
    quadrature = State()
    property_type = State()
    ownership_type = State()
    phone = State()

# REGISTRATION


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


@dp.message_handler(lambda message: message.text not in KEYS, state=userForm.key)
async def process_check_key(message: types.Message):
    """CHECK KEY"""
    return await message.reply(config.OBJECT_TEXT['user']['exc_key'])


@dp.message_handler(lambda message: message.text in KEYS, state=userForm.key)
async def process_key(message: types.Message, state: FSMContext):
    """KEY STATE"""
    
    # start region state
    await userForm.next()
    # update key in state
    await state.update_data(key=message.text)
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['user']['enter_region'])


@dp.message_handler(state=userForm.region)
async def process_region(message: types.Message, state: FSMContext):
    """REGION STATE"""

    async with state.proxy() as data:
        data['region'] = message.text

        # save USER data in db
        user = Users(
            id=str(message.chat.id),
            login=message.chat.username,
            fullname=data['fullname'],
            phone=data['phone'],
            experience=data['experience'],
            job=data['job'],
            key=data['key'],
            region=data['region'])

        db.session.add(user)
        db.session.commit()
        
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
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )


    # finish state
    await state.finish()

# CHECK AUTH USER

# buttons
buttons = ["Продажа", "Лента", "Мои объекты", "Уведомления"]

@dp.message_handler(lambda message: Users.query.filter_by(id=message.chat.id).first() != None 
                    and message.text not in buttons)
async def process_auth(message: types.Message):
    """USER AUTH"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer(config.OBJECT_TEXT['user']['login'], reply_markup=keyboard)


@dp.message_handler(lambda message: Users.query.filter_by(id=message.chat.id).first() == None 
                    and message.text not in buttons)
async def process_not_auth(message: types.Message):
    """USER NOT AUTH"""
    markup = types.ReplyKeyboardRemove()

    await bot.send_message(
        message.chat.id, config.OBJECT_TEXT['user']['not_login'],
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


# FUNCTIONS

# ----------------- SALE --------------------

@dp.message_handler(Text(equals="Продажа"))
async def function_sale(message: types.Message):
    """FUNCTION SALE (SALE STATE)"""
    
    # start objects region state
    await objectsForm.region.set()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['start_add'])
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_region'])

@dp.message_handler(state=objectsForm.region)
async def process_objects_region(message: types.Message, state: FSMContext):
    """OBJECTS REGION STATE"""

    async with state.proxy() as data:
        data['region'] = message.text

    # start objects city state
    await objectsForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_city'])

@dp.message_handler(state=objectsForm.city)
async def process_objects_city(message: types.Message, state: FSMContext):
    """OBJECTS CITY STATE"""

    async with state.proxy() as data:
        data['city'] = message.text

    # start objects address state
    await objectsForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_address'])
    
    
@dp.message_handler(state=objectsForm.address)
async def process_objects_address(message: types.Message, state: FSMContext):
    """OBJECTS ADDRESS STATE"""

    async with state.proxy() as data:
        data['address'] = message.text

    # start objects street state
    await objectsForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_street'])

@dp.message_handler(state=objectsForm.street)
async def process_objects_street(message: types.Message, state: FSMContext):
    """OBJECTS STREET STATE"""

    async with state.proxy() as data:
        data['street'] = message.text

    # start objects stage state
    await objectsForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_stage'])
    
@dp.message_handler(lambda message: not message.text.isdigit(), state=objectsForm.stage)
async def process_stage_invalid(message: types.Message):
    return await message.reply(config.OBJECT_TEXT['objects']['exc_stage'])
    
@dp.message_handler(lambda message: message.text.isdigit(), state=objectsForm.stage)
async def process_objects_stage(message: types.Message, state: FSMContext):
    """OBJECTS STAGE STATE"""

    async with state.proxy() as data:
        data['stage'] = message.text

    # start objects description state
    await objectsForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_description'])

@dp.message_handler(state=objectsForm.description)
async def process_objects_description(message: types.Message, state: FSMContext):
    """OBJECTS DESCRIPTION STATE"""

    async with state.proxy() as data:
        data['description'] = message.text

    # start objects price state
    await objectsForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_price'])
    
    
@dp.message_handler(lambda message: not message.text.isdigit(), state=objectsForm.price)
async def process_price_invalid(message: types.Message):
    return await message.reply(config.OBJECT_TEXT['objects']['exc_price'])


@dp.message_handler(lambda message: message.text.isdigit(), state=objectsForm.price)
async def process_objects_price(message: types.Message, state: FSMContext):
    """OBJECTS PRICE STATE"""

    async with state.proxy() as data:
        data['price'] = message.text

    # start objects quadrature state
    await objectsForm.next()
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_quadrature'])
    
    
property_type_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
property_type_btn_1 = types.InlineKeyboardButton('Вторичка', callback_data='property_type_btn_1')
property_type_btn_2 = types.InlineKeyboardButton('Первичка', callback_data='property_type_btn_2')
property_type_btn_3 = types.InlineKeyboardButton('Новострой', callback_data='property_type_btn_3')
property_type_keyboard.add(property_type_btn_1, property_type_btn_2, property_type_btn_3)

ownership_type_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, selective=True)
ownership_type_btn_1 = types.InlineKeyboardButton('Частная', callback_data='ownership_type_btn_1')
ownership_type_btn_2 = types.InlineKeyboardButton('Государственная', callback_data='ownership_type_btn_2')
ownership_type_keyboard.add(ownership_type_btn_1, ownership_type_btn_2)
    

@dp.message_handler(lambda message: not message.text.replace(',', '.').replace('.','').isdigit(), state=objectsForm.quadrature)
async def process_quadrature_invalid(message: types.Message):
    return await message.reply(config.OBJECT_TEXT['objects']['exc_quadrature'])    

@dp.message_handler(lambda message: message.text.replace(',', '.').replace('.','').isdigit(), state=objectsForm.quadrature)
async def process_objects_quadrature(message: types.Message, state: FSMContext):
    """OBJECTS QUADRATURE STATE"""

    async with state.proxy() as data:
        data['quadrature'] = message.text

    # start objects property type state
    await objectsForm.next()
    
    await bot.send_message(message.chat.id, config.OBJECT_TEXT['objects']['enter_property_type'], reply_markup=property_type_keyboard)

    
@dp.callback_query_handler(Text(startswith="property_type_btn_"), state=objectsForm.property_type)
async def callbacks_property_type(call: types.CallbackQuery, state: FSMContext):
    """CALLBACK PROPERTY TYPE"""
    action = call.data.split('_')[-1]
    
    if action == "1":
        p_type = 'Вторичка'
    elif action == "2":
        p_type = 'Первичка'
    elif action == "3":
        p_type = 'Новострой'
        
    async with state.proxy() as data:
        data['property_type'] = p_type
    
    # start objects ownership type type state
    await objectsForm.next()
        
    await call.answer()
    
    await bot.send_message(call.message.chat.id, p_type)
    await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['objects']['enter_ownership_type']
                           , reply_markup=ownership_type_keyboard)
    
@dp.callback_query_handler(Text(startswith="ownership_type_btn_"), state=objectsForm.ownership_type)
async def callbacks_ownership_type(call: types.CallbackQuery, state: FSMContext):
    """CALLBACK OWNERSHIP TYPE"""
    action = call.data.split('_')[-1]
    
    if action == "1":
        o_type = 'Частная'
    elif action == "2":
        o_type = 'Государственная'
        
    async with state.proxy() as data:
        data['ownership_type'] = o_type
    
    # start objects phone state
    await objectsForm.next()
        
    await call.answer()
    
    await bot.send_message(call.message.chat.id, o_type)
    await bot.send_message(call.message.chat.id, config.OBJECT_TEXT['objects']['enter_phone'])

@dp.message_handler(state=objectsForm.phone)
async def process_objects_phone(message: types.Message, state: FSMContext):
    """OBJECTS PHONE STATE AND SAVE STATE DATA IN DB OBJECTS"""

    async with state.proxy() as data:
        data['phone'] = message.text

        # save Objects data in db
        object = Objects(
            user=str(message.chat.id),
            region=data['region'],
            city=data['city'],
            address=data['address'],
            street=data['street'],
            stage=data['stage'],
            description=data['description'],
            price=data['price'],
            quadrature=data['quadrature'],
            property_type=data['property_type'],
            ownership_type=data['ownership_type'],
            phone=data['phone'])

        db.session.add(object)
        db.session.commit()
        
        # send object data
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text(config.OBJECT_TEXT['objects']['finish_add']),
                md.text('Регион: ', md.bold(data['region'])),
                md.text('Город: ', md.bold(data['city'])),
                md.text('Адрес: ', md.bold(data['address'])),
                md.text('Улица: ', md.bold(data['street'])),
                md.text('Этаж: ', md.bold(data['stage'])),
                md.text('Описание: ', md.bold(data['description'])),
                md.text('Цена: ', md.bold(data['price'] + ' р')),
                md.text('Квадратура: ', md.bold(data['quadrature'] + ' м2')),
                md.text('Тип недвижимости: ', md.bold(data['property_type'])),
                md.text('Тип собственности: ', md.bold(data['ownership_type'])),
                md.text('Телефон: ', md.bold(data['phone'])),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    # finish state
    await state.finish()
    

@dp.message_handler(Text(equals="Лента"))
async def function_feed(message: types.Message):
    """FUNCTION FEED"""
    await message.reply("Лента")


@dp.message_handler(Text(equals="Мои объекты"))
async def function_my_objects(message: types.Message):
    """FUNCTION MY OBJECTS"""
    await message.reply("Мои объекты")


@dp.message_handler(Text(equals="Уведомления"))
async def function_notifications(message: types.Message):
    """FUNCTION NOTIFICATIONS"""
    await message.reply("Уведомления")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
