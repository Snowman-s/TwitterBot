# -*- coding: utf-8 -*-
from tweepy import *
from random import choice
from os.path import abspath, dirname
import account

def auth():
    keys = account.getKeys()
    CONSUMER_KEY = keys[0]
    CONSUMER_SECRET_KEY = keys[1]
    ACCESS_TOKEN = keys[2]
    ACCESS_TOKEN_SECRET = keys[3]

    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return API(auth)

def getFollowers(api):
    friendsList = api.lookup_users(user_ids=api.followers_ids('@BotSnowman'))
    return friendsList

api = auth()

file = open(dirname(__file__) + '\\shabel.txt', 'r', encoding='utf-8')
string = file.readlines()
file.close()

# ツイートのみ
status = choice(string)  # 投稿するツイート

followers = getFollowers(api)
follower = choice(followers)

status = status.format(name=follower.name)

api.update_status(status=status)  # Twitterに投稿
