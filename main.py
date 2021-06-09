# https://lms.skillfactory.ru/

import telebot
from config import TOKEN, KEYS
from extensions import Cryptoconverter, ConvretionException
bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     if not (message.text == "start"):
#         bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=["start", "help"])
def recall_help_messages(message: telebot.types.Message):
    bot.reply_to(message, "Человек должен отправить сообщение боту в виде:\n <имя валюты цену которой он хочет узнать> \
<имя валюты в которой надо узнать цену первой валюты> \
<количество первой валюты>.\n \
Команда /values выводит информацию о всех доступных валютах.")

@bot.message_handler(commands=["values"])
def recall_help_values(message: telebot.types.Message):
    tText = 'Доступные валюты:'
    for kKey in KEYS.keys():
        tText = tText + '\n' + kKey
    bot.reply_to(message, tText)

@bot.message_handler(content_types=["text"])
def convert_der(message: telebot.types.Message):
    # пример запроса доллар евро 40000

    try:
        # область проверки входных параметров
        entered_values = message.text.split(' ')
        len_entered_values = len(entered_values)

        if len_entered_values != 3:
            if len_entered_values > 3:
                raise ConvretionException("Слишком много параметров.")
            else:
                raise ConvretionException("Недостаточно параметров для вычисления.")

        # Область получения данных для расчёта и запуска вычисления
        quote, base, str_amount = entered_values
        total_base = Cryptoconverter.get_price(quote, base, str_amount)

    except ConvretionException as e:
        tText = f'Ошибка клиента.\n{e}'
    except Exception as e:
        tText = f'Ошибка сервера.\n{e}'
    else:
        tText = f'Перевод {str_amount} {quote} в {base} = {total_base}'

        bot.reply_to(message, tText)

if __name__ == '__main__':
    bot.polling(none_stop=True)