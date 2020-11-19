# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 12:44:15 2020

@author: j
"""

from TwitterAPI import TwitterAPI
import json

import product_database

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
    
    # save this tweet response json and the category to the DB! 
    # category should be 'media' or 'tweet'
    
    print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)
    print(str(r.json()))


def postMedia(task_result):
    api = getTwitterApi()
    
    
    # JL TODO - did not load file, is the path correct? 
    
    with open(task_result['filename'], 'rb') as img:
        data = img.read()
    
    r = api.request('media/upload', None, {'media': data})
    
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + r.text)
    print(str(r.json()))
    
    
    # just call postTweet here!
    
    if r.status_code == 200:
        media_id = r.json()['media_id']
        r = api.request('statuses/update', {'status': 'test test test', 'media_ids': media_id})
        print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE: ' + r.text)
    
    
    
    