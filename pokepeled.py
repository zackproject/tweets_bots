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

#Twitter pokehlgame
# Import keys from arguments
keys = None
pokegen = None

print('keys: {0}'.format(sys.argv[1]))
datajsn = sys.argv[1]
pokejsn = sys.argv[2]
with open(datajsn) as f:
  keys = json.load(f)

with open(pokejsn) as j:
  pokegen = json.load(j)


def twitter_api():
    auth = OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    #    api = auth
    return tweepy.API(auth)



def getImageTW(tweetm):
    api = twitter_api()
    status = api.get_status(tweetm, include_entities = True, tweet_mode='extended')
    pokejson = status._json
    image = pokejson['entities']['media'][0]['media_url_https']
    return image



num = 1
with open('pokeg1.json','a') as f:
    f.write('[\n')
    for x in pokegen:
        name = x['url']
        indexID = name.rfind('/')
        namepk = name[indexID+1:len(name)]
        print(namepk)
        #resultat = str('{0}\n'.format(getImageTW(namepk)))
        resultat = "{{'dex': {0}, 'url': '{2}', 'name': '{1}'}},\n".format(num, x['name'],getImageTW(namepk))
        num = num + 1
        f.write(resultat)
    f.write(']')
