# -*- coding: utf-8 -*-
import tweepy
from tweepy import *
from random import choice
from os.path import abspath, dirname
import account


def logError(e):
    file = open(dirname(__file__) + '\\log.txt', 'a', encoding='utf-8')
    file.write(str(e) + "\n")
    import datetime
    file.write(str(datetime.datetime.now))
    file.close()


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
    return api.followers_ids()


def searchBarrageAndRetweet(api, friendsID):
    max_heart = 30
    results = api.search(q=u'弾幕 exclude:retweets')
    for result in results:
        try:
            user_id = result.author.id
            if (user_id in friendsID):
                api.create_favorite(result.id)
        except tweepy.error.TweepError as e:
            logError(e)
        max_heart -= 1
        # 一回に30回までハート
        if (max_heart <= 0):
            return


api = auth()
file = open(dirname(__file__) + '\\shabel.txt', 'r', encoding='utf-8')
string = file.readlines()
file.close()
# ツイートのみ
status = choice(string)  # 投稿するツイート
followersID = getFollowers(api)
followers = api.lookup_users(followersID)
follower = choice(followers)
status = status.format(name=follower.name)
try:
    api.update_status(status=status)  # Twitterに投稿
except tweepy.error.TweepError as e:
    logError(e)
searchBarrageAndRetweet(api, followersID)
