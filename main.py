import telebot
from extensions import APIException, Converter
from config import TOKEN, moneypool, allcurrency
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Приветствую, {message.chat.first_name}, если Вы хотите узнать курсы "
                                      f"валют, то Вам необходимо прописать пару на русском языке с маленькой буквы. "
                                      f"Например, если я хочу узнать сколько стоит 1 доллар, то я напишу 'доллар рубль 1'."
                                      f"Если Вы хотите узнать какие валюты я могу обрабатывать, то пропишите команду'/help'")

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Я могу показать курс следующих валют: {allcurrency}")


@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты на сегодня:'
    for i in moneypool.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)
