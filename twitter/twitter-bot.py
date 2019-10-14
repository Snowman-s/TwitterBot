# -*- coding: utf-8 -*-
from datetime import datetime
from os.path import dirname
from random import choice

import account
import tweepy
from tweepy import *


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
    max_retweet = 5
    now_date = datetime.now()
    results = tweepy.Cursor(api.search,
                            q=u'弾幕 exclude:retweets',
                            since=now_date.strftime('%Y-%m-%d'),
                            count=100
                            ).items()
    for result in results:
        try:
            user_id = result.author.id
            if user_id in friendsID:
                api.retweet(result.id)
                max_retweet -= 1
        except tweepy.error.TweepError as e:
            logError(e)
        # 一回に5回までリツイート
        if max_retweet <= 0:
            return

api = auth()
file = open('shabel.txt', 'r', encoding='utf-8')
string = file.readlines()
file.close()
# ツイートのみ
followersID = getFollowers(api)
followers = api.lookup_users(followersID)
follower = choice(followers)
status = ''
if datetime.now().hour <= 8:
    status = 'おはようございます！今日も一日頑張りましょう！'
elif(datetime.now().hour >= 22):
    status = 'そろそろ眠くなってきました...。おやすみなさい！'
else:
    status = choice(string)  # 投稿するツイート
    status = status.format(name=follower.name)
try:
    api.update_status(status=status)  # Twitterに投稿
except tweepy.error.TweepError as e:
    logError(e)
searchBarrageAndRetweet(api, followersID)
