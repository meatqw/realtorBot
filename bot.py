from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types, executor
import config
from db import Users,  db
import logging

logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# keyboard with "Я не бот" button
btn = types.InlineKeyboardMarkup(text='Я не бот', callback_data='not_bot_btn')
keyboard = types.InlineKeyboardMarkup()
keyboard.add(btn)

@dp.message_handler(commands=['messages'])
async def message_count_hand(message: types.Message):
    """Get message count"""
    user = Users.query.filter_by(id=str(message['from']['id'])).first()
    await bot.send_message(message.chat.id, f"Кол-во сообщений {user.fname}: {user.message_count}")


@dp.message_handler(content_types=["new_chat_members"])
async def new_user(message: types.Message):
    # save user data to base

    id = str(message['new_chat_member']['id'])

    try:
        login = message['new_chat_member']['username']
    except Exception as e:
        login = None
    
    try:
        fname = message['new_chat_member']['first_name']
    except Exception as e:
        fname = None
    
    try:
        lname = message['new_chat_member']['last_name']
    except Exception as e:
        lname = None

    try:
        # save data
        db.session.add(Users(id=id, login=login,
                       fname=fname, lname=lname, status=0))

        db.session.commit()
    except Exception as e:
        print(e)

    await message.answer(f'Привет {fname} 👋', reply_markup=keyboard)


@dp.callback_query_handler(text="not_bot_btn")
async def btn_hand(call: types.CallbackQuery):
    """Processing of btn"""

    # get user by id
    user = Users.query.filter_by(id=str(call['from']['id'])).first()

    if user.status == 0:
        await call.message.delete()

        # switch status to user
        user.status = 1
        db.session.commit()



@dp.message_handler()
async def messages_hand(message: types.Message):
    """Processing of incoming messages"""

    user = Users.query.filter_by(id=str(message['from']['id'])).first()
    if user.status == 0:
        await message.delete()
    else:
        # message count add
        new_message_count = user.message_count + 1
        user.message_count = new_message_count
        db.session.commit()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)