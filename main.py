from random import randint
from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import sys, logging, json
sys.path.insert(0, './')
import generator #All ok

model = generator.train('data\data.txt')

def createPhrase(model=model):
    return ' '.join([generator.generate_sentence(model) for i in range(randint(5, 10))])

f = open(r'token', mode='r')
token = f.read()
f.close()

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton(text='Генерируй', callback_data='gen'))

@dp.message_handler(commands='start')
async def genPhrase(message: types.Message):
    global keyboard
    await message.answer(f'Здравствуйте, {message.from_user.username}, вы попали к боту PhraseCreator.\nТут Вы можете сгенерировать фразу путем нажатия на кнопку Генерируй!\nВсе совпадения с настоящим миром случайны.', reply_markup=keyboard)

@dp.callback_query_handler(text='gen')
async def send_gen(call: types.CallbackQuery):
    global keyboard
    await call.message.answer(str(createPhrase()), reply_markup=keyboard)

@dp.message_handler()
async def getText(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp)