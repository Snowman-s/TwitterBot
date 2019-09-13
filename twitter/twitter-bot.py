# -*- coding: utf-8 -*-
CONSUMER_KEY        = 'sQKCdyci5zlxsNMhshaNV9r4D'
CONSUMER_SECRET_KEY = 'y1uhcN33mkbtWwDbyz6TGhk2dICspExY0zG2QwXW7dPXLX2Yzr'
ACCESS_TOKEN        = '1171993969737076736-4JIUVgjD0g2GVUuuZpS0dWaqqUdOnc'
ACCESS_TOKEN_SECRET = 'LzmcNQ2NeQ8c4v6CBKAcbq7lretQP60ROKfdcKjXAtTdb'
from twitter import *
from random import choice
from os.path import abspath, dirname
#schtasks /create /tn BotTask /tr "'python C:\Users\otiku\OneDrive\ドキュメント\python\twitter\twitter-bot.py'" /sc once
def getFollowers():
    friendsList = []
    next_cursor = 0 
    while True:
        friendsInfo = t.friends.list(cursor=next_cursor)
        for user in friendsInfo['users']:
            friendsList.append({
                    'NumberID':user['id'],
                    'userID':user['screen_name'],
                    'userName':user['name']
                })
        next_cursor = friendsInfo['next_cursor']
        if(next_cursor == 0):
            break
    return friendsList

t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET_KEY))

file = open(dirname(__file__) + '\\shabel.txt', 'r' ,encoding='utf-8')
string = file.readlines()
file.close()

#ツイートのみ
status = choice(string) #投稿するツイート

followers = getFollowers()
follower = choice(followers)

status = status.format(**follower)

t.statuses.update(status=status) #Twitterに投稿
