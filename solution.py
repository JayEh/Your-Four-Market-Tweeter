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

tdc = cards.TopDollarCompanies(products, products_df, rows=25, figsize=(7.5,10))
data = tdc.getData()
tdc.getImage(data)
text = tdc.getTweetText()
print(text)




schedule = {
    'daily': [
        {
            'card': cards.HighThcProducts,
            'time': 9
        },{
            'card': cards.HighCbdProducts,
            'time': 9
        },{
            'card': cards.HighValueProducts,
            'time': 9
        },{
            'card': cards.TopDollarCompanies,
            'time': 9
        }
    ],
    'weekly': [
        {
            'card': 'add the govt urls!',
            'day_of_week': 1,  # monday
            'time': 8
        }
    ]    
}




# and then the govt URLs !!

def main():
    running = True
    
    # check the time
    
    # run any tasks
    
    # sleep a minute?  repeat
    while(running):
        
        
        time.sleep(0.5)
        running = False



if __name__ == '__main__':
    main()

