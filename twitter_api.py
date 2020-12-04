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



def postTweet(task, task_result):
    api = getTwitterApi()
    r = api.request('statuses/update', {'status': task_result['text']})
    product_database.saveTweetToHistory(str(r.json()), 'tweet', task['filename'])
    
    print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)
    
    return r.json()



def postMedia(task, task_result):
    api = getTwitterApi()
    
    with open(task_result['filename'], 'rb') as img:
        data = img.read()
    
    r = api.request('media/upload', None, {'media': data})
    product_database.saveTweetToHistory(str(r.json()), 'media', task['filename'])
    
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + r.text)
    
    if r.status_code == 200:
        return postTweetWithMedia(r.json(), task, task_result)
    
    

def postTweetWithMedia(media_upload_result, task, task_result):
    api = getTwitterApi()
    media_id = media_upload_result['media_id']
    tweet_text = task_result['text']
     
    r = api.request('statuses/update', {'status': tweet_text, 'media_ids': media_id})
    product_database.saveTweetToHistory(str(r.json()), 'tweet', task['filename'])
    
    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE: ' + r.text)
    
    return r.json()
    
    
