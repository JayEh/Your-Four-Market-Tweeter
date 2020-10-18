# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 12:44:15 2020

@author: Jarrett
"""

from TwitterAPI import TwitterAPI
import json

key_location = 'C:\\Python\\Cannabrain\\api_keys.json'

def loadApiKeys():
    with open(key_location, 'r', encoding='utf-8') as file:
        key_json = file.read()
        
    return json.loads(key_json, encoding='utf-8')


def getTwitterApi():
    api_keys = loadApiKeys()
    api = TwitterAPI(
        api_keys['api_key'],
        api_keys['api_key_secret'],
        api_keys['access_token'],
        api_keys['access_token_secret'])
    return api


def postTweet(tweet_text):
    api = getTwitterApi()    
    r = api.request('statuses/update', {'status': tweet_text})
    
    print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)
    
    # str(r.json())
    
    pass




