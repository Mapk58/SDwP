import sys
sys.path.append('../')

import task1
from datetime import datetime
import telebot
import time
import json
import message_handler as mh
import markup_maker as mm
import os
import user_manager as um

token = os.environ.get('BOT_TOKEN')
if token==None:
    print('Environment value trouble! Shutting down...')
    exit()
bot = telebot.TeleBot(token)

# Processing /start command
@bot.message_handler(commands=["start"])
def start(m, res=False):
    um.users.add_user(m.chat.id)
    reply = 'Hello! You have launched the bot created as part of the second task of the SDwP course. Now you can select or create a university, add rooms and assign activities. The source code is here: https://github.com/Mapk58/SDwP'
    bot.send_message(m.chat.id, reply, reply_markup=mm.create_markup(um.users.get_state(m.chat.id)))

# Processing text messages
@bot.message_handler(content_types=["text"])
def handle_text(m):
    print(m.text)
    reply, markup = mh.handle_message(m.chat.id, m)
    bot.send_message(m.chat.id, reply, reply_markup=markup)


while (True):
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print('Connection lost! Retry in 3 sec...')
        print(e)
        time.sleep(3)


