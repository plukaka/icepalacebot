#выложен на hiroku
#plukaka@yandex.kg

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config

import os, json, string

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

async def on_startup(dp):
	await bot.set_webhook(config.URL_APP)

async def on_shutdown(dp):
	await bot.delete_webhook()



#функция для показа в консоли сообщения, пишем тут и добавляем
#внизу в executor on_startup=on_startup
#async def on_startup(_):
#	print('Бот вышел в онлайн')

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
		await message.reply('Мат запрещен!')
		#await message.delete()

#Приветствие нового участника группы
@dp.message_handler(content_types=['new_chat_members'])
async def new_chat(message : types.Message):
	await message.answer('Приветствуем! Ты стал членом нашего дружного вратарского чата! Здесь ты сможешь обсудить, поболтать и поныть. Но учти оскорбления и мат запрещены!')

#Удаление сообщения о том, что пользователь ушел.исключен из группы
@dp.message_handler(content_types=['left_chat_members'])
async def left_chat(message : types.Message):
	await message.delete()


#executor.start_polling(dp, skip_updates = True, on_startup=on_startup)
executor.start_webhook(
	dispatcher=dp,
	webhook_path='',
	on_startup=on_startup,
	on_shutdown=on_shutdown,
	skip_updates=True,
	host="0.0.0.0",
	port=int(os.environ.get("PORT", 5000)))
