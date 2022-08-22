from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import config
from db import db, Users
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
    await bot.send_message(message.chat.id, 'Регистрация\nВведите ФИО')


@dp.message_handler(state=userForm.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    """FULLNAME STATE"""

    async with state.proxy() as data:
        data['fullname'] = message.text

    # start phone state
    await userForm.next()
    await bot.send_message(message.chat.id, 'Введите контактный номер телефона')


@dp.message_handler(state=userForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    """PHONE STATE"""

    async with state.proxy() as data:
        data['phone'] = message.text

    # start expirience state
    await userForm.next()
    await bot.send_message(message.chat.id, 'Введите ваш стаж')


@dp.message_handler(state=userForm.experience)
async def process_experience(message: types.Message, state: FSMContext):
    """EXPERIENCE STATE"""

    async with state.proxy() as data:
        data['experience'] = message.text

    # start job state
    await userForm.next()
    await bot.send_message(message.chat.id, 'Введите информацию о текущем месте работы (если это не АН, то ИП)')


@dp.message_handler(state=userForm.job)
async def process_job(message: types.Message, state: FSMContext):
    """JOB STATE"""

    async with state.proxy() as data:
        data['job'] = message.text

    # start key state
    await userForm.next()
    await bot.send_message(message.chat.id, 'Введите ваш ключ')


@dp.message_handler(lambda message: message.text not in KEYS, state=userForm.key)
async def process_check_key(message: types.Message):
    """CHECK KEY"""
    return await message.reply("Ключ не корректен, повторите ввод")


@dp.message_handler(lambda message: message.text in KEYS, state=userForm.key)
async def process_key(message: types.Message, state: FSMContext):
    """KEY STATE"""

    # start region state
    await userForm.next()
    # update key in state
    await state.update_data(key=message.text)
    await bot.send_message(message.chat.id, 'Введите ваш регион')


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
    await message.answer("Вы авторизованы", reply_markup=keyboard)


@dp.message_handler(lambda message: Users.query.filter_by(id=message.chat.id).first() == None 
                    and message.text not in buttons)
async def process_not_auth(message: types.Message):
    """USER NOT AUTH"""
    markup = types.ReplyKeyboardRemove()

    await bot.send_message(
        message.chat.id, "Вы не авторизованы",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


# FUNCTIONS

@dp.message_handler(Text(equals="Продажа"))
async def function_sale(message: types.Message):
    """FUNCTION SALE (SALE STATE)"""
    
    # start region state
    await objectsForm.fullname.set()
    await bot.send_message(message.chat.id, 'Добавить объект\nВведите Регион')


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
