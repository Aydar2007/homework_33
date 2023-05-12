"""1) Напишите телеграмм бот для IT курса. Бот предназначен для предоставления
информации для пользователя о IT курсах.
В боте есть 5 команды (backend, frontend, uxui, android, ios)
Каждая команда выдает 3 информации (информация о направлении, стоимость курса,
месяц обучения) Пользователь: Нажимает кнопку запустить
Бот: Приветствует пользователя и выдает 5 кнопок (backend, frontend, uxui, android, ios)
Пользователь: Пользователь нажимает backend Бот выдает сообщение:
Backend — это внутренняя часть сайта и сервера и т.д Стоимость 10000 сом в месяц
Обучение: 5 месяц ДОП ЗАДАНИЕ:
2) Загрузить код в GitHub и сделать кнопки для направлений"""


from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os,sqlite3,time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor

load_dotenv('.env')
bot = Bot(os.environ.get('KEY'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR(150),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created VARCHAR(200)
);
""")
cursor.connection.commit()
 
inline_buttons1 = [
    InlineKeyboardButton('Backend', callback_data='inline_text1'),
    InlineKeyboardButton('Frontend', callback_data='inline_text2'),
    InlineKeyboardButton('UIUX', callback_data='inline_text3'),
    InlineKeyboardButton('Android', callback_data='inline_text4')
]
inline1 = InlineKeyboardMarkup().add(*inline_buttons1)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    cursor=db.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES (
            {message.from_user.id},
            '{message.from_user.username}',
            '{message.from_user.first_name}',
            '{message.from_user.last_name}',
            '{time.ctime()}'
        )""")
        cursor.connection.commit()
    await message.answer(f'Привет {message.from_user.full_name} '
                         f'Я могу предоставить информацию про програмирование в нашей компании "Geeks"'
                         , reply_markup=inline1)
@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == "inline_text1":
        await Backend (call.message)
    elif call.data == "inline_text2":
        await Frontend (call.message)
    elif call.data == "inline_text3":
        await UIUX (call.message)
    elif call.data == "inline_text4":
        await Android (call.message)

@dp.message_handler(commands=['Backend'], state=None)
async def Backend(message: types.Message):
    await message.answer(f'Backend — это внутренняя часть продукта, которая находится на сервере и скрыта от пользователей. Для её разработки могут использоваться самые разные языки, например, Python, PHP, Go, JavaScript, Java, С#.')
    await message.answer(f'Стоимость курса 10000 сом в месяц , но при хорошем обучении выдается скидка с 1000 до 2000 сом')
    await message.answer(f'Обучение длится 5 месяцов',)
@dp.message_handler(commands=['Frontend'], state=None)
async def Frontend(message: types.Message):
    await message.answer(f'Front-end разработка — это создание клиентской части сайта. Front-end разработчик занимается версткой шаблона сайта и созданием пользовательского интерфейса. Обычно front-end разработчик — это мастер на все руки. Он просто обязан обладать талантом дизайнера, быть искусным верстальщиком и хорошим программистом.')
    await message.answer(f'Стоимость курса 10000 сом в месяц , но при хорошем обучении выдается скидка с 1000 до 2000 сом')
    await message.answer(f'Обучение длится 5 месяцов')
@dp.message_handler(commands=['Android'], state=None)
async def Android(message: types.Message):
    await message.answer(f'Android-разработчик создает приложения для устройств на операционной системе Android. Он пишет код, работает над интерфейсом и дизайном, тестирует приложение и исправляет баги, а также адаптирует его под разные модели устройств (которых у Android великое множество).')
    await message.answer(f'Стоимость курса 10000 сом в месяц , но при хорошем обучении выдается скидка с 1000 до 2000 сом')
    await message.answer(f'Обучение длится 6 месяцов')
@dp.message_handler(commands=['UIUX'], state=None)
async def UIUX(message: types.Message):
    await message.answer(f'UX/UI-дизайн — это проектирование удобных, понятных и эстетичных пользовательских интерфейсов. Чтобы разобраться, какие задачи решает специалист в этой сфере, нужно понять, что такое UX и UI. UX — user experience — переводится на русский язык как «пользовательский опыт».')
    await message.answer(f'Стоимость курса 10000 сом в месяц , но при хорошем обучении выдается скидка с 1000 до 2000 сом')
    await message.answer(f'Обучение длится 3 месяцов')

executor.start_polling(dp)
