# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 12:49:04 2020

@author: Jarrett
"""

from weed_tweeter import WebScraper
import cards

scraper = WebScraper()
products, products_df = scraper.getProductDataFromWeb()


# data1 = HighThcProducts(products, products_df).getData()


highThcProductsCard = cards.HighThcProducts(products, products_df, rows=15)
data = highThcProductsCard.getData()
highThcProductsCard.getImage(data)

text = highThcProductsCard.getTweetText()
print(text)
