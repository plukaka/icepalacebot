from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os, json, string

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

#функция для показа в консоли сообщения, пишем тут и добавляем
#внизу в executor on_startup=on_startup
async def on_startup(_):
	print('Бот вышел в онлайн')

'''******** КЛИЕНТСКАЯ ЧАСТЬ **********'''

'''@dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
	try: #обработка ошибки если юзер не акцептовал бот ранее
		await bot.send_message(message.from_user.id, 'Приветствую! Чем могу помочь?')
		await message.delete() #удаляем сообщение чтобы оно не висело
	except: 
		await message.reply('Общение с ботом через ЛС, напишите ему: \n https://t.me/')'''

'''******** ОБЩАЯ ЧАСТЬ **********'''

@dp.message_handler()
async def echo_send(message : types.Message):
	if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
		.intersection(set(json.load(open('cenz.json')))) != set():
		await message.reply('Маты запрещены!')
		#await message.delete()

#Приветствие нового участника группы
@dp.message_handler(content_types=['new_chat_members'])
async def new_chat(message : types.Message):
	await message.answer('Добро пожаловать!')

#Удаление сообщения о том, что пользователь ушел.исключен из группы
@dp.message_handler(content_types=['left_chat_members'])
async def left_chat(message : types.Message):
	await message.delete()


executor.start_polling(dp, skip_updates = True, on_startup=on_startup)

