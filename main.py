import requests
from bs4 import BeautifulSoup as Bs
import telebot
from telebot import types
from config import TOKEN,API


def get_info():
     r = requests.get(url='https://ria.ru/')
     soup = Bs(r.text,'html.parser')
     items = soup.find_all('span',class_='cell-list__item-title')
     for i in items:
          yield i.text
a = get_info()
# print(next(a))
# print(next(a))


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def first(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Поиск','Команды')
    bot.send_message(message.chat.id,'Привет {}'.format(message.from_user.first_name),reply_markup=markup)

@bot.message_handler(commands=['город'])
def city(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Бишкек','Москва','Алматы','/назад')
    bot.send_message(message.chat.id,"Выберите город для получения информацции о погоде",reply_markup=markup)

@bot.message_handler(commands=['новости'])
def news(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,next(a),reply_markup=markup)

@bot.message_handler(commands=['стоп'])
def stop(message):
    remove_markup =types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,'До новых встреч',reply_markup=remove_markup)

@bot.message_handler(commands=['назад'])
def back(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Поиск','Команды')
        bot.send_message(message.chat.id,'И снова здравствуйте {}'.format(message.from_user.first_name),reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Команды':
          markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
          markup.row('/город','/стоп','/новости','/назад')
          bot.send_message(message.chat.id,'Выбери команду',reply_markup=markup)
    elif message.text == '/новости':
          markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
          bot.send_message(message.chat.id,next(a))
    elif message.text == '/назад':
          markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
          markup.row('Поиск','Команды')
          bot.send_message(message.chat.id,'И снова здравствуйте {}'.format(message.from_user.first_name),reply_markup=markup)
    elif message.text == 'Поиск':
         bot.send_message(message.chat.id,'<b>выберите город</b>',parse_mode='html')
    else:
         try:
              file = open('weather.txt','w')
              CITY = message.text.upper()
              URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API}"
              data = requests.get(url = URL)
              file.write(data.text)
              responce = requests.get(url=URL).json()
              info = {
                   'city':CITY,
                   'temp':responce['main']['temp'],
                   'weather': responce['weather'][0]['description'],
                   'wind':responce['wind']['speed']
              }
              information = f"<b>{CITY.upper()}</b>\n-<b>Температура : {info['temp']}</b>\n-<b>Погода : {info['weather']}</b>\n-<b>Скорость ветра : {info['wind']}</b>"
              bot.send_message(message.chat.id,information,parse_mode='html')
         except:   
              print("что то пошло не так")



bot.polling(non_stop=True)