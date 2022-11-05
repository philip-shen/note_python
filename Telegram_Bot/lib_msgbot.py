from datetime import datetime
import configparser
import telegram, requests

__all__ = [
    'telegram_chat_dot',
    'get_telegram_chat_id',
    'telegram_bot_sendtext',
]

class telegram_chat_dot:

    def __init__(self, config_ini, opt_verbose='OFF'):
        self.config_ini= config_ini
        self.opt_verbose= opt_verbose

        config = configparser.ConfigParser()
        config.read(self.config_ini, 'utf-8')
        self.TELEGRAM_TOKEN = str(config.get('login', 'api_key'))

        self.bot = telegram.Bot(self.TELEGRAM_TOKEN)
        
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None
            raise(self.update_id)
        #bot = telegram.Bot(TELEGRAM_TOKEN) 
        
    def get_telegram_chat_id(self):
        #bot = telegram_token#telegram.Bot(bot_token)
        
        self.chat_id= self.bot.get_updates()[0].message.chat.id
            

    def telegram_bot_sendtext(self, bot_message):
        
        time_stamp= '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        send_text = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}".\
                        format(self.TELEGRAM_TOKEN, self.chat_id, bot_message)
        response = requests.get(send_text)

        return response.json()

def get_telegram_chat_id(telegram_token):
    bot = telegram.Bot(telegram_token)        
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    chat_id= bot.get_updates()[0].message.chat.id
    
    return chat_id

def telegram_bot_sendtext(telegram_token, bot_chatID, bot_message, opt_verbose='OFF'):
        
    time_stamp= '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
    send_text = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}".\
                format(telegram_token, bot_chatID, bot_message)
    response = requests.get(send_text)
    
    if opt_verbose.lower() == 'on':
        msg = '\n telegram_bot_sendtext: {} '.format(send_text)
        logger.info(msg)

    return response.json()    