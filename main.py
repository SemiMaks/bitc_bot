from datetime import datetime

import requests
import telebot

from auth_data import token


def get_data():
    req = requests.get('https://yobit.net/api/3/ticker/btc_rur')
    response = req.json()
    # print(response)
    sell_price = response['btc_rur']['sell']
    print(f"Текущее время: {datetime.now().strftime('%Y-%M-%D %H:%M')}\nСтоимость битка в руб: {sell_price}")


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['старт'])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет, напиши 'биток' для поиска цены BTC")

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.text.lower() == 'биток':
            try:
                req = requests.get('https://yobit.net/api/3/ticker/btc_rur')
                response = req.json()
                sell_price = response['btc_rur']['sell']
                bot.send_message(
                    message.chat.id,
                    f"Текущее время: {datetime.now().strftime('%Y-%M-%D %H:%M')}\nСтоимость битка в руб: {sell_price}"
                )
            except Exception as err:
                print(err)
                bot.send_message(message.chat.id, 'Не вышло....')
        else:
            bot.send_message(message.chat.id, 'Не понял...')

    bot.polling()


if __name__ == '__main__':
    get_data()
    telegram_bot(token)
