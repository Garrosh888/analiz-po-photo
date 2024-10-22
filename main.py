import telebot
import wether
from telebot import types
from random import randint
import requests
import analiz_photo
bot = telebot.TeleBot("6550167691:AAEN5v7BqNWO01bvBGbilVm3zDUYmXRrnEU")
info_photo = ""
#markup - вертуальное меню клавиотура для чат бота
#item - кнопки меню
#@bot.message_handler - декоратор он нам нужен что бы отлавлевать определеные события
#wb - запись бенарного файла , все что не текстовый файл это бенарный файл
#
#

@bot.message_handler(commands=["start"])#то что будет написано ниже первое сообщение чат бота


def start(message):# начальное меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("случайное число")
    item2 = types.KeyboardButton("курс валют")
    item3 = types.KeyboardButton("погода сейчас")
    item4 = types.KeyboardButton("анализ фотографии")
    markup.add(item1,item2,item3,item4)
    msg = f"привет {message.from_user.first_name} {message.from_user.last_name}"
    bot.send_message(message.chat.id,msg,reply_markup=markup)


@bot.message_handler(content_types=["text"])#он отлавливает любой текст

def get_user_text(message):
    global info_photo
    info_photo = ""
    if message.text == "как дела" or  message.text == "как ты" or message.text == "як справи":

        bot.send_message(message.chat.id,"все шикарно")
    elif message.text == "класуха":#как делать ответ с фоткой
        photo = open ("klasuha.png","rb" )#rb = открыть , открыть файл в бинарном режиме
        bot.send_photo(message.chat.id,photo)
    elif message.text =="спокойной ночи":#это я дз делаю
        bot.send_message(message.chat.id,"спокойной ")
    elif message.text == "случайное число":
        bot.send_message(message.chat.id,f"твое случайное число {randint(100000,999999)}")
    elif message.text == "курс валют":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("usd,euro,aed,usdt,btc,efr ")
        back = types.KeyboardButton("back")
        markup.add(item1,back)
        bot.send_message(message.chat.id,"выберете",reply_markup = markup)
    elif message.text == "back":#кнопка назад

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("случайное число")
        item2 = types.KeyboardButton("курс валют")
        item3 = types.KeyboardButton("погода сейчас")
        item4 = types.KeyboardButton("анализ фотографии")
        markup.add(item1,item2,item3,item4)
        msg = f"вы вернулис в главное меню"
        bot.send_message(message.chat.id,msg,reply_markup=markup)
    elif message.text == "хочу идеальный мир":
        photo = open("dubai.png","rb")#rb = открыть , открыть файл в бинарном режиме
        bot.send_photo(message.chat.id,photo)
    elif message.text == "погода сейчас":
        bot.send_message(message.chat.id,wether.get_wether())
    elif message.text == "анализ фотографии":
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("узнать возраст")
        item2 = types.KeyboardButton("узнать эмоции")
        item3 = types.KeyboardButton("узнать расу")
        item4 = types.KeyboardButton("узнать все")
        item5 = types.KeyboardButton("back")
        markup.add(item1,item2,item3,item4,item5)
        bot.send_message(message.chat.id,"выберете какую информацию хотите узнать ",reply_markup = markup)
    elif message.text == "узнать возраст":
        info_photo = "age"
        bot.send_message(message.chat.id,"отправте фотографию для анализа")
    elif message.text == "узнать эмоции":
        info_photo = "emotion"
        bot.send_message(message.chat.id,"отправте фотографию для анализа")
    elif message.text == "узнать расу":
        info_photo = "race"
        bot.send_message(message.chat.id, "отправте фотографию для анализа")
    elif message.text == "узнать все":
        info_photo = "all"
        bot.send_message(message.chat.id, "отправте фотографию для анализа")


@bot.message_handler(content_types=["photo"])#декоратор отлавливает событие отправки фотографии

def get_user_photo(message):

    if info_photo != "" :
        photo = message.photo[-1]
        filename = f"{photo.file_id}.jpg"
        photo_id = photo.file_id
        bot.send_message(message.chat.id,"фотография получена")
        file_info = bot.get_file(photo_id)
        file_path = file_info.file_path
        photo_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
        res = requests.get(photo_url)

        with open( f"photos\{filename}.jpg",'wb') as new_file:
            new_file.write(res.content)
        bot.reply_to(message,"фотография сохранена ")#это времено
        if info_photo == "age":
            try:
                age = analiz_photo.face_analiz_age(f"photos\{filename}.jpg")
                bot.send_message(message.chat.id,age[0]["age"])
            except:
                bot.send_message(message.chat.id,"отправте другую фотографию")
        elif info_photo == "emotion":
            try:
                emotion = analiz_photo.face_analiz_emotion(f"photos\{filename}.jpg")
                bot.send_message(message.chat.id, emotion[0]["dominant_emotion"])
            except:
                bot.send_message(message.chat.id, "отправте другую фотографию")
        elif info_photo == "race":
            try:
                race = analiz_photo.face_analiz_race(f"photos\{filename}.jpg")
                bot.send_message(message.chat.id, race[0]["dominant_race"])
            except:
                bot.send_message(message.chat.id, "отправте другую фотографию")
        elif info_photo == "all":
            try:
                race = analiz_photo.face_analiz_race(f"photos\{filename}.jpg")
                emotion = analiz_photo.face_analiz_emotion(f"photos\{filename}.jpg")
                age = analiz_photo.face_analiz_age(f"photos\{filename}.jpg")
                result_age = age[0]["age"]
                result_emotion = emotion[0]["dominant_emotion"]
                result_race = race[0]["dominant_race"]
                info = f"возраст: {result_age},раса: {result_race},эмоции: {result_emotion} "
                bot.send_message(message.chat.id, info)
            except:
                bot.send_message(message.chat.id, "отправте другую фотографию")


bot.polling(none_stop = True) #что б бот всегда роботал

