import time
import configparser
import telegram, requests
from datetime import datetime
import threading
import lib_msgbot
import logger_generate

if __name__ == '__main__':
    logger_config = {
    "logging_level": 'INFO',
    "log_file_path": './logs/{0:%Y%m%d_%H%M%S}.log'.format(datetime.now()),
    "log_format": '%(asctime)s - %(levelname)s : %(message)s',
    "backupCount": 7,
    "when": 'D',
    "encoding": 'utf-8',
    }
    
    t0 = time.time()
    local_time = time.localtime(t0)
    #msg = 'Start Time is {}/{}/{} {}:{}:{}'
    #print(msg.format( local_time.tm_year,local_time.tm_mon,local_time.tm_mday,\
    #                        local_time.tm_hour,local_time.tm_min,local_time.tm_sec))    

    msg= 'Start Test!'
    logger = logger_generate.generate(logger_config, "")
    logger.info(msg)

    config_file = './config.ini'
    
    local_msgbot= lib_msgbot.telegram_chat_dot(config_file)
    local_msgbot.get_telegram_chat_id()
    str_msg= "* Let's go *"

    for idx in range(0,6,1):
        str_msg= "* Let's go {}th time(s)*".format(idx+1)
        #local_msgbot.telegram_bot_sendtext(str_msg)

        task_telegram= threading.Thread(target= local_msgbot.telegram_bot_sendtext, \
                                args= ([str_msg]) )      

        task_telegram.start()     
        #task_telegram.join()  

    """
    config = configparser.ConfigParser()
    config.read(config_file, 'utf-8')
    TELEGRAM_TOKEN = str(config.get('login', 'api_key'))
    chat_id = lib_msgbot.get_telegram_chat_id(TELEGRAM_TOKEN)
    
    message2 = lib_msgbot.telegram_bot_sendtext(TELEGRAM_TOKEN, chat_id, "* Let's go *")
    if message2['ok']:
        print(message2['result']['text'])
    """
    
    #bot_token.send_message(chat_id = chat_id, text =str_msg)
    time_consumption= time.time() - t0
    msg = 'Time Consumption: {:.1f} seconds.'.format( time_consumption)
    #print(msg)
    logger.info(msg)