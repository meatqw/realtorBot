from aiogram.utils import executor
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

# REGISTRATION


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """START HANDLING"""

    # start fullname state
    await userForm.fullname.set()
    await bot.send_message(message.chat.id, 'Регистрация\nВведите ФИО')

    # save user data to base (registration)


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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
