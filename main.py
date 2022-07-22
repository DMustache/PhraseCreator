import generator  # All ok
from random import randint
from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sys
import logging
sys.path.insert(0, './')

BOT_NAME = "PhraseCreator"

MODEL = generator.train(r'data\data.txt')


def createPhrase(model=MODEL):
    return ' '.join(
        [generator.generate_sentence(model) for i in range(randint(5, 10))]
    )


@dp.message_handler(commands='start')
async def genPhrase(message: types.Message):
    global keyboard
    await message.answer(f'''Здравствуйте,
    {message.from_user.username}, вы попали к боту {BOT_NAME}.
    Тут Вы можете сгенерировать фразу путем нажатия на кнопку Генерируй!
    Все совпадения с настоящим миром случайны.''', reply_markup=keyboard)


@dp.callback_query_handler(text='gen')
async def send_gen(call: types.CallbackQuery):
    global keyboard
    await call.message.answer(str(createPhrase()), reply_markup=keyboard)


@dp.message_handler()
async def getText(message: types.Message):
    await message.answer(message.text)


def main():
    executor.start_polling(dp)
    f = open(r'token', mode='r')
    token = f.read()
    f.close()

    bot = Bot(token=token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(level=logging.INFO)

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text='Генерируй', callback_data='gen'))


if __name__ == '__main__':
    main()
