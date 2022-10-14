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

token = os.environ.get('BOT_TOKEN')
if token==None:
    print('Environment value trouble! Shutting down...')
    exit()
bot = telebot.TeleBot(token)
users = {}
with open('data/users.json') as json_file:
    users = json.load(json_file)
# Processing /start command
@bot.message_handler(commands=["start"])
def start(m, res=False):
    users[m.chat.id] = 'very_beginning'
    reply = 'Hello! You have launched the bot created as part of the second task of the SDwP course. Now you can select or create a university, add rooms and assign activities. The source code is here: https://github.com/Mapk58/SDwP'
    bot.send_message(m.chat.id, reply, reply_markup=mm.create_markup(users[m.chat.id]))
    with open("data/users.json", "w") as outfile:
        json.dump(users, outfile)

# Processing text messages
@bot.message_handler(content_types=["text"])
def handle_text(m):
    print(m.text)
    reply, markup = mh.handle_message(m.chat.id, users[str(m.chat.id)], m)
    bot.send_message(m.chat.id, reply, reply_markup=markup)


while (True):
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print('Connection lost! Retry in 3 sec...')
        print(e)
        time.sleep(3)


