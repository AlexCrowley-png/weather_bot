import telebot
import requests
import datetime

from conf import telegram_bot_token, owm_api_token

Wtoken = owm_api_token
Btoken = telegram_bot_token
sticker = "CAACAgIAAxkBAAIB5l-hX7PKlahqDxV585Ic-L5FPRT6AAL0AAOrV8QLJwnAPhI8xdkeBA"
url = 'http://api.openweathermap.org/data/2.5/weather?'
bot = telebot.TeleBot(Btoken)

def answer_constr(Wanswer):
	answer = "Температура в выбраной точке: "+ str(Wanswer['main']['temp']) + '\nОщущается как: ' + str(Wanswer['main']['feels_like'])
	answer+= "\nДавление: " + str(int(Wanswer['main']['pressure']*0.750062)) +" мм рт ст" + "\nВлажность: " + str(Wanswer['main']['humidity']) + "%"
	answer+= "\nВетер: "
	if Wanswer['wind']['deg'] >337.5 or Wanswer['wind']['deg'] <= 22.5:
		answer+= "северный, "
	elif Wanswer['wind']['deg'] >22.5 and Wanswer['wind']['deg'] <= 67.5:
		answer+= "северо-восточный, "
	elif Wanswer['wind']['deg'] >67.5 and Wanswer['wind']['deg'] <= 112.5:
		answer+= "восточный, "
	elif Wanswer['wind']['deg'] >112.5 and Wanswer['wind']['deg'] <= 157.5:
		answer+= "юго-восточный, "
	elif Wanswer['wind']['deg'] >157.5 and Wanswer['wind']['deg'] <= 202.5:
		answer+= "южный, "
	elif Wanswer['wind']['deg'] >202.5 and Wanswer['wind']['deg'] <= 247.5:
		answer+= "юго-западный, "
	elif Wanswer['wind']['deg'] >247.5 and Wanswer['wind']['deg'] <= 292.5:
		answer+= "западный, "
	elif Wanswer['wind']['deg'] >292.5 and Wanswer['wind']['deg'] <= 337.5:
		answer+= "северо-западный, "
	answer+= str(Wanswer['wind']['speed']) + ' м/с'
	answer+= "\nОблачность: " + str(Wanswer['clouds']['all']) + " %"
	return answer

@bot.message_handler(commands=['start'])

def start_message(message):
	answer = "Привет, " + message.chat.first_name + ". Вы можете отправить мне название наcеленного пункта или точку на карте, что бы узнать температуру."
	bot.send_message(message.chat.id, answer)
	print(message.chat.username + " joined the chat")


@bot.message_handler(content_types = ['text'])

def send_message(message):
	date = datetime.datetime.fromtimestamp(message.date)
	print(message.chat.username + " send " + str(message.content_type) + str(date)  + '....' + message.text)
	responce = requests.get(url + "q=" + message.text + "&appid=" + Wtoken + "&units=metric")
	Wanswer = responce.json()
	if Wanswer['cod']==200 :
		answer = answer_constr(Wanswer)
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
	Wanswer = responce.json()
	print(url + 'lat=' + str(message.location.latitude) + "&lon=" + str(message.location.longitude) + "&appid=" + Wtoken + "&units=metric")
	answer = answer_constr(Wanswer)
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
