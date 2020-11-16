# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:49:04 2020

@author: j
"""

from weed_tweeter import WebScraper
from datetime import datetime
import cards
import time
import twitter_api
import product_database

scraper = WebScraper()
products, products_df = scraper.getProductDataFromWeb()

highThcProductsCard = cards.HighThcProducts(products, products_df, rows=25, figsize=(7.5,10), filename='high_thc_products')
data = highThcProductsCard.getData()
highThcProductsCard.getImage(data)
text = highThcProductsCard.getTweetText()
print(text)

highCbdProductsCard = cards.HighCbdProducts(products, products_df, rows=25, figsize=(7.5,10), filename='high_cbd_products')
data = highCbdProductsCard.getData()
highCbdProductsCard.getImage(data)
text = highCbdProductsCard.getTweetText()
print(text)

highValueProductsCard = cards.HighValueProducts(products, products_df, rows=25, figsize=(7.5,10), filename='high_value_products')
data = highValueProductsCard.getData()
highValueProductsCard.getImage(data)
text = highValueProductsCard.getTweetText()
print(text)

tdc = cards.TopDollarProducts(products, products_df, rows=25, figsize=(7.5,10), filename='top_dollar_products')
data = tdc.getData()
tdc.getImage(data)
text = tdc.getTweetText()
print(text)

urls = cards.GovernmentURLs()
text = urls.getTweetText()



class TaskRunner():
    def __init__(self):
        
        hour = 17
        
        rows = 25
        figsize=(7.5,10)
        
        self.schedule = {
            'daily': [
                {
                    'card': cards.HighThcProducts,
                    'hour': hour,
                    'rows': rows,
                    'figsize': figsize,
                    'filename': 'HighThcProducts'
                },{
                    'card': cards.HighCbdProducts,
                    'hour': hour,
                    'rows': rows,
                    'figsize': figsize,
                    'filename': 'HighCbdProducts'
                },{
                    'card': cards.HighValueProducts,
                    'hour': hour,
                    'rows': rows,
                    'figsize': figsize,
                    'filename': 'HighValueProducts'
                },{
                    'card': cards.TopDollarProducts,
                    'hour': hour,
                    'rows': rows,
                    'figsize': figsize,
                    'filename': 'TopDollarProducts'
                }
            ],
            'weekly': [
                {
                    'card': 'add the govt urls!',
                    'day_of_week': 1,  # monday
                    'hour': 8
                }
            ]
        }
    
    
    def getRunnableTasks(self):
        # get the current time
        now = datetime.now() # device timezone
        
        # check against the schedule
        tasks = [x for x in self.schedule['daily'] if x['hour'] == now.hour]
        
        # JL TODO
        # has the task already run? skip if so.  finish this !  and test method 
        product_database.hasTaskRunToday
        
        
        return tasks
            
            
    
    # products=None, products_df=None, rows=None, figsize=None, filename=None
    def runTask(self, task):
        card = task['card'](products, products_df, task['rows'], task['figsize'], task['filename'])
        
        data = card.getData()
        card.getImage(data)
        text = card.getTweetText()
        
        return  {
            'data': data,
            'filename': task['filename'],
            'text': text
            }




def main():
    runner = TaskRunner()
    running = True
    
    while(running):
        tasks = runner.getRunnableTasks()
        for t in tasks:
            results = runner.runTask(t)

            tweet_text = results[2]

            # take these results and tweet them !
            twitter_api.postTweet(tweet_text)
            
            # be kind to the api
            time.sleep(5)
            
        
        time.sleep(60)
        running = False



if __name__ == '__main__':
    main()

