import requests
import json
import sys
import re
from datetime import date
from time import sleep
from PIL import Image
import tweepy
from tweepy import OAuthHandler
import argparse
def allTipus(jsonTipus):
    llista = []
    for x in jsonTipus:
        llista.append(x["type"]["name"])

    return "({})".format(' '.join(str(x) for x in llista))


def dexNumBasedDay(dateInicial):
    # El dia que empieza el bot
    d0 = dateInicial
    d1 = date.today()
    delta = d1 - d0
    # Los dias que han pasado desde que inicio
    return delta.days


def sentenceForTweet(jsonC):
    name = jsonC["name"].capitalize()
    tipus = allTipus(jsonC["types"])
    hp = jsonC["stats"][0]["base_stat"]
    attack = jsonC["stats"][1]["base_stat"]
    defense = jsonC["stats"][2]["base_stat"]
    special_attack = jsonC["stats"][3]["base_stat"]
    special_defense = jsonC["stats"][4]["base_stat"]
    speed = jsonC["stats"][5]["base_stat"]
    best = hp + attack + defense + special_attack + special_defense + speed
    return "{0} {1}\nHP: {2}\nAttack: {3}\nDefense: {4}\nSp.Attack: {5}\nSp.Defense: {6}\nSpeed: {7}\nTotal: {8}".format(
        name, tipus, hp, attack, defense, special_attack, special_defense, speed, best)


def saveImage(urlImage, nameAndPath):
    response = requests.get(urlImage)
    file = open(nameAndPath, "wb")
    file.write(response.content)
    file.close()


def addBackground(ruta, background, pathSave):
    # Open overlay image
    img = Image.open(ruta)
    img_w, img_h = img.size
    background = Image.open(background)
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w), (bg_h - img_h) // 2)
    nono = background.paste(img, offset, img)
    nono = background.convert('RGB')
    nono.save(pathSave)


def twitter_api():
    auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    #    api = auth
    return tweepy.API(auth)


def tweet_image(alt_img, filename, message, num):
    api = twitter_api()
    media_ids = []
    try:
        res = api.media_upload(filename)
        #Add alt text
        api.create_media_metadata(res.media_id, alt_img)
        media_ids.append(res.media_id)
        api.update_status(media_ids=media_ids, status=message)
    except Exception as e:
        directMessage("ERROR Tweet [{0}]".format(str(e)), num)


def directMessage(textMessage, userID):
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(
        keys["twitter"]["consumer_key"], keys["twitter"]["consumer_secret"])
    # set access to user's access key and access secret
    auth.set_access_token(keys["twitter"]["access_token"],
                          keys["twitter"]["access_token_secret"])
    api = tweepy.API(auth)  # calling the api
    recipient_id = userID  # ID of the recipient Twitter Username number
    text = textMessage  # text to be sent
    direct_message = api.send_direct_message(
        recipient_id, text)  # sending the direct message
    # printing the text of the sent direct message
    print(direct_message.message_create['message_data']['text'])

#Twitter pokehlgame
# Import keys from arguments
keys = None
print('keys: {0}'.format(sys.argv[1]))
datajsn = sys.argv[1]
with open(datajsn) as f:
  keys = json.load(f)

# El num dex depende de cuantos dias han pasado desde la fecha indicada
ndex = dexNumBasedDay(date(2021, 11, 3))
#ndex = 586
#Modificado para por Total en vez de Best
url = "https://pokeapi.co/api/v2/pokemon/{0}".format(ndex)
pathImage = "images/image.png"
pathFondo = "images/fondo.png"
r = requests.get(url=url)
jsonPoke = r.json()
num = 1407831450888683521

image = jsonPoke["sprites"]["other"]["official-artwork"]["front_default"]
# Descargar imagen
saveImage(image, pathImage)
sleep(0.5)
# Sobrescribir imagen con fondo
addBackground(ruta=pathImage, background=pathFondo, pathSave=pathImage)
alt_name = jsonPoke["name"]
#Tweet con imagen pokemon hlgame
tweet_image(alt_name, pathImage, sentenceForTweet(jsonPoke), num)
print('#{0} {1}'.format(ndex, alt_name))
