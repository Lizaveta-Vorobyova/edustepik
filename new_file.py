from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ContentType
from aiogram.filters import Command
from aiogram.types import Message
import os
from dotenv import load_dotenv
from aiogram.filters import BaseFilter

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
CODEWORD = os.getenv('CODEWORD')

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словарь для хранения состояний пользователей
users = {}

class Status(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not users[message.from_user.id]['status']

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer(f'Здравствуйте!\nМеня зовут Доктор Софи!\nЭто бот-сомнолог😴\nДля активации бота введите кодовое слово')
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'status': False,
            'ИМТ': None,
            'Рост': 0,
            'Вес': 0,
            'ФИО': '',
            'да': 0,
            'нет': 0
        }
    print(users[message.from_user.id])

# Функция обработки текстовых сообщений
@dp.message(F.text.in_([f'{CODEWORD}']))
async def process_codeword(message: Message):
    users[message.from_user.id]['status'] = True
    await message.answer("Бот успешно активирован! Введите Ваше Имя и Фамилию.")


# Функция обработки неверного кодового слова
@dp.message(Status())
async def wrong_codeword(message: Message):
    if not users[message.from_user.id]['status']:
        await message.answer("Неверное кодовое слово. Попробуйте еще раз.")


# Функция обработки ФИО
@dp.message()
async def process_fio(message: Message):
    if users[message.from_user.id]['status'] and not users[message.from_user.id]['ФИО']:
        users[message.from_user.id]['ФИО'] = message.text
        await message.answer(f"Спасибо, {message.text}! Бот готов к работе.")
        print(users[message.from_user.id])


@dp.message(Command(commands="cancel"))
async def reboot(message: Message):
    await message.answer('Working')
    users[message.from_user.id]['status'] = False
    for i in users[message.from_user.id][1:]:
        users[message.from_user.id][i] = None
    await message.answer("Вы сбросили все данные. Чтобы начать контактировать с ботом нажмите /start")
    print(users[message.from_user.id])

# Регистрация обработчиков
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(reboot, Command(commands='cancel'))
dp.message.register(process_codeword)
dp.message.register(wrong_codeword)
dp.message.register(process_fio)



# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
