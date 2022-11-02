import configparser
import telegram
import requests
import datetime

def get_telegram_chat_id(bot_token):
    bot = telegram.Bot(bot_token)
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    chat_id= bot.get_updates()[0].message.chat.id
    
    return chat_id

def telegram_bot_sendtext(bot_token, bot_chatID, bot_message):

    time_stamp= '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    """send_text = 'https://api.telegram.org/bot' + bot_token + \
                '/sendMessage?chat_id=' + bot_chatID + \
                '&parse_mode=Markdown&text=' + bot_message
    """
    send_text = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}".\
                    format(bot_token, bot_chatID, bot_message)
    response = requests.get(send_text)

    return response.json()


if __name__ == '__main__':

    config_file = './config.ini'
    config = configparser.ConfigParser()
    config.read(config_file, 'utf-8')
    TELEGRAM_TOKEN = str(config.get('login', 'api_key'))
    chat_id =get_telegram_chat_id(TELEGRAM_TOKEN)

    message2 = telegram_bot_sendtext(TELEGRAM_TOKEN, chat_id, "你可以開始了")
    if message2['ok']:
        print(message2['result']['text'])
    #bot.send_message(chat_id = chat_id, text ='你可以開始了')
