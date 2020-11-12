# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:49:04 2020

@author: j
"""

from weed_tweeter import WebScraper
from datetime import datetime
import cards
import time


scraper = WebScraper()
products, products_df = scraper.getProductDataFromWeb()

highThcProductsCard = cards.HighThcProducts(products, products_df, rows=25, figsize=(7.5,10))
data = highThcProductsCard.getData()
highThcProductsCard.getImage(data)
text = highThcProductsCard.getTweetText()
print(text)

highCbdProductsCard = cards.HighCbdProducts(products, products_df, rows=25, figsize=(7.5,10))
data = highCbdProductsCard.getData()
highCbdProductsCard.getImage(data)
text = highCbdProductsCard.getTweetText()
print(text)

highValueProductsCard = cards.HighValueProducts(products, products_df, rows=25, figsize=(7.5,10))
data = highValueProductsCard.getData()
highValueProductsCard.getImage(data)
text = highValueProductsCard.getTweetText()
print(text)

tdc = cards.TopDollarProducts(products, products_df, rows=25, figsize=(7.5,10))
data = tdc.getData()
tdc.getImage(data)
text = tdc.getTweetText()
print(text)



class TaskRunner():
    def __init__(self):
        self.schedule = {
            'daily': [
                {
                    'card': cards.HighThcProducts,
                    'hour': 9
                },{
                    'card': cards.HighCbdProducts,
                    'hour': 9
                },{
                    'card': cards.HighValueProducts,
                    'hour': 9
                },{
                    'card': cards.TopDollarProducts,
                    'hour': 9
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
        cards = [x['card'] for x in self.schedule['daily'] if x['hour'] == now.hour]
        
        # check if it's already been done today (db query)
        already_run = False
        
        # run or skip as required
        if already_run == False:
            ans = 1 + 1
            
            # run task
            # update db with results
            
            
    
    
    def runTask(self, card):
        data = card.getData()
        image = card.getImage(data)
        text = card.getTweetText()
        return (data, image, text)




def main():
    runner = TaskRunner()
    running = True
    
    while(running):
        tasks = runner.getRunnableTasks()
        for t in tasks:
            results = runner.runTask(t)

            # take these results and tweet them !
            
        
        time.sleep(0.5)
        running = False



if __name__ == '__main__':
    main()

