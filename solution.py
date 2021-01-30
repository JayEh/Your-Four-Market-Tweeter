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

from constants import DEBUG


# highThcProductsCard = cards.HighThcProducts(products, products_df, rows=25, figsize=(7.5,10), filename='high_thc_products')
# data = highThcProductsCard.getData()
# highThcProductsCard.getImage(data)
# text = highThcProductsCard.getTweetText()
# print(text)

# highCbdProductsCard = cards.HighCbdProducts(products, products_df, rows=25, figsize=(7.5,10), filename='high_cbd_products')
# data = highCbdProductsCard.getData()
# highCbdProductsCard.getImage(data)
# text = highCbdProductsCard.getTweetText()
# print(text)

# highValueProductsCard = cards.HighValueProducts(products, products_df, rows=25, figsize=(7.5,10), filename='high_value_products')
# data = highValueProductsCard.getData()
# highValueProductsCard.getImage(data)
# text = highValueProductsCard.getTweetText()
# print(text)

# tdc = cards.TopDollarProducts(products, products_df, rows=25, figsize=(7.5,10), filename='top_dollar_products')
# data = tdc.getData()
# tdc.getImage(data)
# text = tdc.getTweetText()
# print(text)

# urls = cards.GovernmentURLs()
# text = urls.getTweetText()


class TaskRunner():
    def __init__(self):
        
        hour = 14
        rows = 25
        figsize=(10,10)
        
        
        self.schedule = {
            'daily': [
                {
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
                    'card': cards.HighThcProducts,
                    'hour': hour,
                    'rows': rows,
                    'figsize': figsize,
                    'filename': 'HighThcProducts'
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
        # has the task already run? skip if so.  finish this !  and test method 
        tasks = [task for task in self.schedule['daily'] if task['hour'] == now.hour and not product_database.hasTaskRunToday(task, now)]
        
        return tasks


    def runTask(self, task, products, products_df):
        card = task['card'](products, products_df, task['rows'], task['figsize'], task['filename'])
        
        data = card.getData()
        card.getImage(data)
        text = card.getTweetText()
        
        return  {
            'data': data,
            'filename': card.filename,
            'text': text
            }



def main():
    scraper = WebScraper()
    products, products_df = scraper.getProductDataFromWeb()
    
    runner = TaskRunner()
    running = True
    
    while(running):
        tasks = runner.getRunnableTasks()
        for t in tasks:
            task_result = runner.runTask(t, products, products_df)
            
            if DEBUG == False:
                response_json = twitter_api.postMedia(t, task_result)
                print(response_json)
                
                # be kind to the api, sleep a bit
                time.sleep(1)
            
        running = False
        # time.sleep(60)

if __name__ == '__main__':
    main()

