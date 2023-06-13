# -*- coding: utf-8 -*-
import os
import requests
import tweepy
from tweepy import OAuthHandler
from time import sleep
import datetime
import sys
import json

# Import keys from arguments
keys = None
print('keys: {0}'.format(sys.argv[1]))
datajsn = sys.argv[1]
with open(datajsn) as f:
  keys = json.load(f)
print(str(keys))

monthList = ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Setiembre', 'Octubre',
             'Noviembre', 'Diciembre']


def callBirthday(day, month):
    characterList = []
    headers = {
        "User-Agent": keys['user_agent']}
    url = 'https://www.animecharactersdatabase.com/api_series_characters.php?month={1}&day={0}'.format(day, month)
    # Lets test what headers are sent by sending a request to HTTPBin
    r = requests.get(url=url, headers=headers)
    jsonC = r.json()
    # print(jsonC)
    for x in jsonC['characters']:
        c1 = Character(x['name'], x['origin'], x['character_image'], day, monthList[month])
        characterList.append(c1)
        # print('Hoy {0} de {1} cumple aos {2} de {3}. \nÂ¡Felicidades! {4}'.format(day, monthList[month], x['name'],  x['origin'], x['character_image']))
    return characterList


def twitter_api():
    auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    #    api = auth
    return tweepy.API(auth)


def strNumCharacter(num, day, month):
    return "Hoy {0} de {1} cumple años {2} personajes.\n¡En mi perfil felicitamos a tod@s!\n#AnimeBirthday #animetwt #anitwt #{3}".format(str(day), str(month), str(num), getSignZodiac(day, month))

def tweet_only(message):
    try:
        api = twitter_api()
        api.update_status(message)
        print("Inicio - {0}".format(message))
    except Exception as e:
        directMessage("ERROR Inicial [{0}]".format(str(e)),keys['md_username'])
        print("ERROR {0}".format(str(e)))


def tweet_image(alt_img, url, message, num):
    api = twitter_api()
    media_ids = []
    filename = 'images/birth.jpg'
    request = requests.get(url, stream=True)
    try:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        res = api.media_upload(filename)
        #Add alt text on image before upload
        api.create_media_metadata(res.media_id, alt_img)
        media_ids.append(res.media_id)
        api.update_status(media_ids=media_ids, status=message)
        os.remove(filename)
    except Exception as e:
        directMessage("ERROR Tweet [{0}]".format(str(e)), num)
        print("Unable to download image")

def directMessage(textMessage, userID):
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    # set access to user's access key and access secret
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    # calling the api
    api = tweepy.API(auth)
    # ID of the recipient Twitter Username number
    recipient_id = userID
    # text to be sent
    text = textMessage
    # sending the direct message
    direct_message = api.send_direct_message(recipient_id, text)
    # printing the text of the sent direct message
    print(direct_message.message_create['message_data']['text'])

def getSignZodiac(day, month):
    month = month.lower()
    astro_sign = 'animebirthday'
    if month == 'diciembre':
        astro_sign = 'sagitario' if (day < 22) else 'capricornio'
    elif month == 'enero':
        astro_sign = 'capricornio' if (day < 20) else 'acuario'
    elif month == 'febrero':
        astro_sign = 'acuario' if (day < 19) else 'piscis'
    elif month == 'marzo':
        astro_sign = 'piscis' if (day < 21) else 'aries'
    elif month == 'abril':
        astro_sign = 'aries' if (day < 20) else 'tauro'
    elif month == 'mayo':
        astro_sign = 'tauro' if (day < 21) else 'geminis'
    elif month == 'junio':
        astro_sign = 'gemini' if (day < 21) else 'cancer'
    elif month == 'julio':
        astro_sign = 'cancer' if (day < 23) else 'leo'
    elif month == 'agosto':
        astro_sign = 'leo' if (day < 23) else 'virgo'
    elif month == 'septiembre':
        astro_sign = 'virgo' if (day < 23) else 'libra'
    elif month == 'octubre':
        astro_sign = 'libra' if (day < 23) else 'escorpio'
    elif month == 'noviembre':
        astro_sign = 'escorpio' if (day < 22) else 'sagitario'
    return astro_sign

class Character:
    def __init__(self, name, anime, imageUrl, day, month):
        self.name = name
        self.anime = anime
        self.imageUrl = imageUrl
        self.day = day
        self.month = month

    def getImageUrl(self):
        return self.imageUrl

    def toString(self):
        return 'Hoy {0} de {1} cumple años {2} de {3}.\n¡Felicidades!\nhttps://zackapps.carrd.co'.format(
            self.day, self.month, self.name, self.anime)

dt = datetime.datetime.today()
day = dt.day
month = dt.month
charList = callBirthday(day, month)
num = 0
tiempo = (len(charList) * 15) / 60
directMessage("{0} de {1}\n- {2} tweets\n- Tiempo {3} min".format(day, monthList[month], len(charList), tiempo),
              keys['md_username'])
sleep(1)
tweet_only(strNumCharacter(len(charList), day, monthList[month]))
sleep(1)
for x in charList:
    try:
        num += 1
        print('[{0}-{1}] {2} Image: {3}'.format(num, len(charList), x.toString(), x.getImageUrl()))
        #if num==3:
        tweet_image('Imagen de {0}'.format(x.name), x.getImageUrl(), x.toString(), num)
        sleep(15)
    except:
        print('ERROR tuiteando')
        directMessage("ERROR [{0}-{1}]".format(num, len(charList)), keys['md_username'])
print("PC Completado [{0}-{1}]".format(num, len(charList)))
directMessage("Completado [{0}-{1}]".format(num, len(charList)), keys['md_username'])

