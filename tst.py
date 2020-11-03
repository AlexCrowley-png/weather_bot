import telebot
import requests
import datetime

from conf import telegram_bot_token, owm_api_token

Wtoken = owm_api_token
Btoken = telegram_bot_token
sticker = "CAACAgIAAxkBAAIB5l-hX7PKlahqDxV585Ic-L5FPRT6AAL0AAOrV8QLJwnAPhI8xdkeBA"
url = 'http://api.openweathermap.org/data/2.5/weather?'
bot = telebot.TeleBot(Btoken)

@bot.message_handler(commands=['start'])

def start_message(message):
	answer = "Привет, " + message.chat.first_name + ". Вы можете отправить мне название наcеленного пункта или точку на карте, что бы узнать температуру."
	bot.send_message(message.chat.id, answer)
	print(message.chat.username + " joined the chat")


@bot.message_handler(content_types = ['text'])

def send_echo(message):
	date = datetime.datetime.fromtimestamp(message.date)
	print(message.chat.username + " send " + str(message.content_type) + str(date)  + '....' + message.text)
	responce = requests.get(url + "q=" + message.text + "&appid=" + Wtoken + "&units=metric")
	answer = responce.json()
	if answer['cod']==200 :
		answer = "Температура в городе " + message.text + ": "+ str(answer['main']['temp']) + '\nОщущается как: ' + str(answer['main']['feels_like'])
		bot.send_message(message.chat.id, answer)
	else:
		answer = "Такой город не найден. Введите правильное название на английском или русском языке, или отправьте геопозицию, где хотите узнать погоду."
		bot.send_message(message.chat.id, answer)



@bot.message_handler(content_types = ['location'])

def send_weather(message):
	date = datetime.datetime.fromtimestamp(message.date)
	print(message.chat.username + " send " + str(message.content_type) + str(date))
	req = url + "lat=" + str(message.location.latitude) + "&lon=" + str(message.location.longitude) + "&appid=" + Wtoken + "&units=metric"
	responce = requests.get(req)
	answer = responce.json()
	print(url + str(message.location.latitude) + "&lon=" + str(message.location.longitude) + "&appid=" + Wtoken + "&units=metric")
	answer = "Температура в выбраной точке: "+ str(answer['main']['temp']) + '\nОщущается как: ' + str(answer['main']['feels_like'])
	bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types =  ['sticker'])

def send_sticker(message):
	date = datetime.datetime.fromtimestamp(message.date)
	print(message.chat.username + " send " + str(message.content_type)  + str(date))
	answer = message.chat.first_name + ", для того, что бы узнать температуру мне необходимо название города или точка на карте, а не стикер..."
	bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAIB5l-hX7PKlahqDxV585Ic-L5FPRT6AAL0AAOrV8QLJwnAPhI8xdkeBA")
	bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types =  ['file', 'document', 'audio', 'photo', 'animation', 'video', 'video_note', 'voice', 'contact', 'file', 'poll'])

def send_err(message):
	date = datetime.datetime.fromtimestamp(message.date)
	answer = "Я могу обработать только название города на русском или английском языке, или геопозицию."
	print(message.chat.username + " send " + str(message.content_type)  + str(date))
	bot.send_message(message.chat.id, answer)


bot.polling()
