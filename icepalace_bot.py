#выложен на hiroku
#plukaka@yandex.kg

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config

import os, json, string, uuid
import speech_recognition as sr
import soundfile as sf
import requests
import subprocess
import datetime

logfile = str(datetime.date.today()) + '.log'
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
	await bot.set_webhook(config.URL_APP)

async def on_shutdown(dp):
	await bot.delete_webhook()

'''******** АУДИО **********'''
async def audio_to_text(dest_name: str):
# Функция для перевода аудио , в формате ".vaw" в текст
	r = sr.Recognizer()
# тут мы читаем наш .vaw файл
	message = sr.AudioFile(dest_name)
	with message as source:
		audio = r.record(source)
	result = r.recognize_google(audio, language="ru_RU") # здесь можно изменять язык распознавания
	return result

@dp.message_handler(content_types=['voice'])
async def get_audio_messages(message):
# Основная функция, принимает голосовуху от пользователя
	try:
		print("Started recognition...")
# Ниже пытаемся вычленить имя файла, да и вообще берем данные с мессаги
		file_info = bot.get_file(message.voice.file_id)
		path = file_info.file_path # Вот тут-то и полный путь до файла (например: voice/file_2.oga)
		fname = os.path.basename(path) # Преобразуем путь в имя файла (например: file_2.oga)
		doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))# Получаем и сохраняем присланную голосвуху (Ага, админ может в любой момент отключить удаление айдио файлов и слушать все, что ты там говоришь. А представь, что такую бяку подселят в огромный чат и она будет просто логировать все сообщения [анонимность в телеграмме, ахахаха])
		with open(fname+'.oga', 'wb') as f:
			f.write(doc.content) # вот именно тут и сохраняется сама аудио-мессага
		process = subprocess.run(['ffmpeg', '-i', fname+'.oga', fname+'.wav'])# здесь используется страшное ПО ffmpeg, для конвертации .oga в .vaw
		result = audio_to_text(fname+'.wav') # Вызов функции для перевода аудио в текст, а заодно передаем имена файлов, для их последующего удаления
		bot.send_message(message.from_user.id, format(result))
	except sr.UnknownValueError as e:
		bot.send_message(message.from_user.id,  "Прошу прощения, но я не разобрал сообщение, или оно поустое...")
		with open(logfile, 'a', encoding='utf-8') as f:
			f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) + ':Message is empty.\n')
	except Exception as e:
		bot.send_message(message.from_user.id,  "Что-то пошло через жопу, но наши смелые инженеры уже трудятся над решением... \nДа ладно, никто эту ошибку исправлять не будет, она просто потеряется в логах.")
		with open(logfile, 'a', encoding='utf-8') as f:
			f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(message.from_user.username) +':'+ str(message.from_user.language_code) +':' + str(e) + '\n')
	finally:
		os.remove(fname+'.wav')
		os.remove(fname+'.oga')

# async def recognise(filename):
#     with sr.AudioFile(filename) as source:
#         audio_text = r.listen(source)
#         try:
#             text = r.recognize_google(audio_text,language=language)
#             print('Converting audio transcripts into text ...')
#             print(text)
#             return text
#         except:
#             print('Sorry.. run again...')
#             return "Sorry.. run again..."

# @dp.message_handler(content_types=['voice'])
# async def voice_processing(message):
# 	filename = str(uuid.uuid4())
# 	file_name_full="./voice/"+filename+".ogg"
# 	file_name_full_converted="./ready/"+filename+".wav"
# 	file_info = bot.get_file(message.voice.file_id)
# 	downloaded_file = bot.download_file(file_info.file_path)
# 	with open(file_name_full, 'wb') as new_file:
# 		new_file.write(downloaded_file)
# 	os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
# 	text=recognise(file_name_full_converted)
# 	bot.reply_to(message, text)
# 	os.remove(file_name_full)
# 	os.remove(file_name_full_converted)


@dp.message_handler(content_types=['new_chat_members'])
async def new_chat(message : types.Message):
	await message.answer('Приветствуем! Ты стал членом нашего дружного вратарского чата! Здесь ты сможешь обсудить, поболтать и поныть. Но учти оскорбления и мат запрещены!')


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
