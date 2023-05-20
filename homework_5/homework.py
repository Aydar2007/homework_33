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
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os,sqlite3,time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from states import SignUpState
from aiogram.dispatcher import FSMContext

load_dotenv('.env')
bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS titles(
    id INT,
    title VARCHAR (500),
    address VARCHAR(100),
    time VARCHAR(100)
);
""")
cursor.connection.commit()
db3 = sqlite3.connect('database.db')
cursor = db3.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR(150),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    tel VARCHAR (10)
);
""")
cursor.connection.commit()


db2 = sqlite3.connect('database.db')
cursor = db2.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS address(
    id INT,
    address_latitude VARCHAR(1000),
    address_longitude VARCHAR(1000)
);
""")
cursor.connection.commit()

 
inline_buttons1 = [
    InlineKeyboardButton('Отправить номер', callback_data='inline_text1'),
    InlineKeyboardButton('Оправить локацию', callback_data='inline_text2'),
    InlineKeyboardButton('Заказать еду', callback_data='inline_text3'),
]
inline1 = InlineKeyboardMarkup().add(*inline_buttons1)


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

    await message.answer(f'Здравствуйте {message.from_user.full_name} '
                         , reply_markup=inline1)
@dp.callback_query_handler()
async def inline(call):
    if call.data == "inline_text1":
        await telefon (call.message)
    elif call.data == "inline_text2":
        await location (call.message)
    elif call.data == "inline_text3":
        await eat (call.message)
    


@dp.message_handler(commands=['telefon'], state=None)
async def telefon(message: types.Message):
    await message.answer("Напишите cвой номер для связи(Телефонный номер в формате c 0:)")
    if len(message.text) == 13 and message.text[1:].isdigit() and message.text[0] == "+":
        sql = '''UPDATE users SET tel = ? WHERE id = {message.from_user.id}'''
        cursor = cursor.connection()
        cursor.execute(sql,message.text)
        cursor.connection.commit()
        await message.answer(reply_markup=inline1)
        await SignUpState.tel.set()

    

@dp.message_handler(commands=['location'], state=None)
async def location(message: types.Message,):
    await message.answer("Укажите ширину")
    await SignUpState.address_latitude.set()
@dp.message_handler(state=SignUpState.address_latitude)
async def get_location(message:types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите долгату:")
    await SignUpState.address_longitude.set()
@dp.message_handler(state=SignUpState.address_longitude)
async def get_longitude(message:types.Message, state:FSMContext):
    await state.update_data(address_longitude=message.text)
    await message.answer("OK")
    user_data = await storage.get_data(user=message.from_user.id)
    cursor = db2.cursor()
    cursor.execute(f"""INSERT INTO address VALUES(
        {message.from_user.id},
        '{user_data["address_latitude"]}',
        '{user_data['address_longitude']}'
    );""")
    cursor.connection.commit()

@dp.message_handler(commands=['eat'], state=None)
async def eat(message: types.Message):
    await message.answer(f"Введите заголовок:",reply_markup=inline1)
    await SignUpState.title.set()

executor.start_polling(dp)