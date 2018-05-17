import os
import sys
import telepot
from settings import token, start_msg
from telepot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from time import sleep
import requests
import json

# State for user
user_state = {}


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Check user state
    try:
        user_state[chat_id] = user_state[chat_id]
    except:
        user_state[chat_id] = 0

    # start command
    if 'text' in msg and msg['text'] == '/start':
        bot.sendMessage(chat_id, start_msg, parse_mode='Markdown')

    if 'text' in msg and msg['text'] == '/cerca':
        msg = "Scrivi la località (solo USA)"
        markup = ReplyKeyboardMarkup(keyboard=[["Brooklyn", "Staten Island"], ["Queens", "New York"], ["Bronx"]
                                               ])
        bot.sendMessage(chat_id, msg, reply_markup=markup)
        user_state[chat_id] = 1

    elif 'text' in msg and msg['text'] == '/cercagps':
        msg = "Inviami la tua posizione"
        bot.sendMessage(chat_id, msg)
        user_state[chat_id] = 1

    elif user_state[chat_id] == 1:

        if content_type == 'text':
            try:
                r = requests.get(
                    url='https://hotspotsusa-api.herokuapp.com/hotspots/:city=' + str(msg['text']))
                json_data = r.json()

                for i in range(2, 7):
                    # takes links from the JSON
                    nome = json_data['features'][i * 3]['properties']['city'] + '\n' +\
                        json_data['features'][i * 3]['properties']['ssid'] + '\n' +\
                        json_data['features'][i * 3]['properties']['type'] + '\n' +\
                        json_data['features'][i * 3]['properties']['name']
                    lat = json_data['features'][i * 3]['properties']['lat']
                    lon = json_data['features'][i * 3]['properties']['lon']

                    bot.sendMessage(chat_id, nome, reply_markup=ReplyKeyboardRemove(
                        remove_keyboard=True))
                    bot.sendLocation(chat_id, lat, lon)

            except:
                bot.sendMessage(chat_id, "Errore API", reply_markup=ReplyKeyboardRemove(
                    remove_keyboard=True))

        elif content_type == 'location':

            try:
                # send location
                response = requests.get('http://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(
                    msg['location']['latitude']) + ',' + str(msg['location']['longitude']))
                resp_json_payload = response.json()
                a = str(resp_json_payload['results'][0]
                        ['address_components'][2]['long_name'])

                if a == 'West Bronx':
                    a = 'Bronx'

                try:
                    r = requests.get(
                        url='https://hotspotsusa-api.herokuapp.com//hotspots/:city=' + str(a))
                    json_data = r.json()

                    for i in range(2, 7):
                        # takes links from the JSON
                        nome = json_data['features'][i * 3]['properties']['city'] + '\n' +\
                            json_data['features'][i * 3]['properties']['ssid'] + '\n' +\
                            json_data['features'][i * 3]['properties']['type'] + '\n' +\
                            json_data['features'][i * 3]['properties']['name']

                        lat = json_data['features'][i * 3]['properties']['lat']
                        lon = json_data['features'][i * 3]['properties']['lon']

                        bot.sendMessage(chat_id, nome, reply_markup=ReplyKeyboardRemove(
                            remove_keyboard=True))
                        bot.sendLocation(chat_id, lat, lon)

                except:
                    bot.sendMessage(chat_id, "Errore API", reply_markup=ReplyKeyboardRemove(
                        remove_keyboard=True))
            except:
                 bot.sendMessage(chat_id, "Errore API Google, riprova...")


# Main
print("Avvio Tonyco97Bot")


# Start working
try:
    bot = telepot.Bot(token)
    bot.message_loop(on_chat_message)
    while(1):
        sleep(10)
finally:
    print("esci")
