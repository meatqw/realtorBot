import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import config

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# создаём форму и указываем поля
class Form(StatesGroup):
    name = State() 
    age = State() 
    gender = State() 


# Начинаем наш диалог
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await Form.name.set()
    await message.reply("Привет! Как тебя зовут?")


# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


# Сюда приходит ответ с именем
@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.reply("Сколько тебе лет?")


# Проверяем возраст
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
async def process_age_invalid(message: types.Message):
    return await message.reply("Напиши возраст или напиши /cancel")

# Принимаем возраст и узнаём пол
@dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(age=int(message.text))

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("М", "Ж")
    markup.add("Другое")

    await message.reply("Укажи пол (кнопкой)", reply_markup=markup)


# Проверяем пол
@dp.message_handler(lambda message: message.text not in ["М", "Ж", "Другое"], state=Form.gender)
async def process_gender_invalid(message: types.Message):
    return await message.reply("Не знаю такой пол. Укажи пол кнопкой на клавиатуре")


# Сохраняем пол, выводим анкету
@dp.message_handler(state=Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
        markup = types.ReplyKeyboardRemove()

        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Hi! Nice to meet you,', md.bold(data['name'])),
                md.text('Age:', md.code(data['age'])),
                md.text('Gender:', data['gender']),
                sep='\n',
            ),
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN,
        )

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)