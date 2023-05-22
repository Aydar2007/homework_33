"""DODO PIZZA AIOGRAM BOT
Описание: Напишите телеграмм бот для Dodo Pizza для заказа еды и пиццы
Требования: Написать бот с помощью библиотеки aiogram и база данных на sqlite3
База: В базе должны быть 3 таблицы.
Это users(список клиентов) в котором есть колонны first_name, last_name, username,
id_user, phone_number.
И также при вызове команды /start проверьте существует ли данный пользователь в
нашей базе. Если его нету в базе данных, обязательно запишите его
Еще есть вторая таблица address, в котором есть колонны id_user,
address_longitude, address_latitude где сам пользователь передает свои координаты
доставки и это записывается в базу
Третья таблица orders для заказа еды и в нем есть три колонны title,
address_destination, date_time_order. Где пользователь может заказать еду
РАБОТА С БОТОМ:
Пользователь запускает команду и ему приходит сообщение “Здравствуйте
{message.from_user.full_name}” и если его нету в таблице users, записываете его. И
также с этим сообщением будет 3 inline кнопки (Отправить номер, Отправить
локацию, Заказать еду)
Если пользователь нажимает на “Отправить номер”, то вы берете номер и
добавляете его номер в таблицу users
Если пользователь нажимает на “Отправить локацию”, то вы конечно берете его
локацию записываете в таблицу address
Если пользователь нажимает на “Заказать еду”, то вы получите его заказ(title), адрес
доставки(address), время заказа автоматически учитывается c встроенными модулями
для работы с временем(date_time_order) и записываете данные в orders
ДОП ЗАДАНИЕ:
Загрузить код в GitHub c .gitignore
ПРИМЕЧАНИЕ:
Можете сделать домашнее задание до субботы(20 мая)"""

from dotenv import load_dotenv
from aiogram.types import KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup
import os,sqlite3,time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from states import SignUpState , PhoneState,LocationState,LocationState2
from aiogram.dispatcher import FSMContext

load_dotenv('.env')
bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = sqlite3.connect('db.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE  IF NOT EXISTS orders(
    id INT,
    title VARCHAR (500),
    time 
);
""")
cursor.connection.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR(150),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    tel VARCHAR (100)
);
""")
cursor.connection.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS address(
    id INT,
    address_latitude VARCHAR(1000),
    address_longitude VARCHAR(1000)
);
""")
cursor.connection.commit()

 
location_buttons = [
    KeyboardButton("Отправить локацию", request_location=True)
]
locations = ReplyKeyboardMarkup(resize_keyboard=True).add(*location_buttons)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_data = await storage.get_data(user=message.from_user.id)
    cursor=db.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES (
            {message.from_user.id},
            '{message.from_user.username}',
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{0}'

        );""")
        cursor.connection.commit()

    await message.answer(f'Здравствуйте {message.from_user.full_name}, мои команды /commands ')
    


@dp.message_handler(commands=['phone'], state=None)
async def get_phone_number (message:types.Message):
    await message.answer("Ваши телефоные данные:")
    await PhoneState.phone.set()
    
@dp.message_handler(state=PhoneState)
async def update_user_number(message:types.Message,state:FSMContext):
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET tel = {message.text} WHERE id = {message.from_user.id};")
    cursor.connection.commit()

@dp.message_handler(commands=["location"],state=None)
async def location(message:types.Message):
     await message.answer(f"""Укажите ваше местоположение 
с помощью /latitude (широта) и /longitude (долгота)""")

@dp.message_handler(commands=['latitude'], state=None)
async def get_location(message: types.Message):
        await message.answer("Ваша широта")
        await LocationState.address_latitude.set()
        cursor=db.cursor()
        cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
        res = cursor.fetchall()
        if res == []:
            cursor.execute(f"""INSERT INTO address VALUES (
                {message.from_user.id},
                {0},
                {0}

            );""")
            cursor.connection.commit()
@dp.message_handler(state=LocationState)
async def update_user_number(message:types.Message,state:FSMContext):
    cursor = db.cursor()
    cursor.execute(f"UPDATE address SET address_latitude = {message.text} WHERE id = {message.from_user.id};")
    cursor.connection.commit()


@dp.message_handler(commands=["longitude"],state=None)
async def gets_location(message:types.message):
        await message.answer("Ваша долгота")
        await LocationState2.address_longitude.set()
@dp.message_handler(state=LocationState2)
async def update_user_number(message:types.Message,state:FSMContext):
    cursor = db.cursor()
    cursor.execute(f"UPDATE address SET address_longitude = {message.text} WHERE id = {message.from_user.id};")
    cursor.connection.commit()

@dp.message_handler(commands=['eat'], state=None)
async def eat(message: types.Message):
    await message.answer(f"Введите заголовок:")
    await SignUpState.title.set()
@dp.message_handler(state=SignUpState)
async def update_user_number(message:types.Message,state:FSMContext):
    cursor = db.cursor()
    cursor.execute(f"""INSERT INTO orders VALUES (
            {message.from_user.id},
            '{message.text}',
            '{time.ctime()}'

        );""")
    cursor.connection.commit()


executor.start_polling(dp)