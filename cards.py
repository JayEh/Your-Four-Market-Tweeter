# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:17:18 2020

@author: jarre
"""

import matplotlib.pyplot as plt
import numpy as np


# inherit this class
class TweetCard():
    def __init__(self, products, products_df):
        self.products = products
        self.products_df = products_df




class HighThcProducts(TweetCard):
    """
    Which companies have the highest THC products (the highest average), and what are those products?
    """
    
    def getData(self):
        # this one is a little different... lots of people will be at like 28% and 
        # to be fair we should randomly select from that pool so everyone gets a chance
        
        highest_thc = self.products_df.groupby(['Brand','DisplayName']).mean()
        highest_thc = highest_thc.sort_values(by=['thc_max'], ascending=False)
        
        top_thc = list(highest_thc['thc_max'][:10].values)
        
        min_val = min(top_thc)
        
        # take from highest THC where greater than min val, want those all the time
        report_rows = highest_thc[highest_thc['thc_max'] > min_val]
        
        # then filter highest_thc on the min_val, and fill in the remaining slots from here
        min_rows = highest_thc[highest_thc['thc_max'] == min_val]
        min_rows_prob = np.full(len(min_rows), 1/len(min_rows))
        
        
        
        # this is a little off but the general idea.  min_rows is not a 1D array
        additional_rows = np.random.choice(min_rows, p=min_rows_prob, size=10-len(report_rows))
        
        
        
        
        report_rows = report_rows + additional_rows
        
        # do this once all the products are selected in the special way
        # top_brands = list(report_rows.index)
        # top_thc = list(report_rows['thc_max'].values)
        
        return list(zip(top_brands, top_thc))
    
    def getImage(self, data):
        fig, ax = plt.subplots()

        companies = [d[0] for d in data] # y axis
        avg_thc = [d[1] for d in data]   # x axis
        
        y_pos = np.arange(len(companies))
        
        ax.barh(y_pos, avg_thc, align='center')
        ax.set_ylabel('Brand')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies)        
        ax.invert_yaxis()  # sort desc
        
        ax.set_xticks([])
        ax.set_title('AGLC - Highest Average THC Content')
        plt.show()





class HighThcCompanies(TweetCard):
    def getData(self):
        grouped_by_brand = self.products_df.groupby(['Brand']).mean()
        grouped_by_brand = grouped_by_brand.sort_values(by=['thc_avg'], ascending=False)
        
        top_brands = list(grouped_by_brand[:10].index)
        top_thc = list(grouped_by_brand['thc_avg'][:10].values)
        
        return list(zip(top_brands, top_thc))
    
    def getImage(self, data):
        fig, ax = plt.subplots()

        companies = [d[0] for d in data] # y axis
        avg_thc = [d[1] for d in data]   # x axis
        
        y_pos = np.arange(len(companies))
        
        ax.barh(y_pos, avg_thc, align='center')
        ax.set_ylabel('Brand')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies)        
        ax.invert_yaxis()  # sort desc
        
        ax.set_xticks([])
        ax.set_title('AGLC - Highest Average THC Content')
        plt.show()
        
        # save the figure
        # return it?




class HighValueCompanies(TweetCard):
    def getData(self):
        grouped_by_brand = self.products_df.groupby(['Brand']).mean()
        grouped_by_brand = grouped_by_brand.sort_values(by=['dollar_per_gram'])
        
        top_brands = list(grouped_by_brand[:10].index)
        top_dpg = list(grouped_by_brand[:10]['dollar_per_gram'])
        
        return list(zip(top_brands, top_dpg))
    
    def getImage(self, data):
        fig, ax = plt.subplots()
        
        top_brands = [d[0] for d in data]
        dpg = [d[1] for d in data]

        y_pos = np.arange(len(top_brands))
        
        ax.barh(y_pos, dpg, align='center')
        ax.set_ylabel('Brand')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_brands)        
        ax.invert_yaxis()  # sort desc
        
        # need to get the $ amounts drawn onto this chart!
        
        
        ax.xaxis.set_visible(False)
        ax.set_title('AGLC - Lowest Average Dollar Per Gram')
        plt.show()
        
        # save the figure
        # return it?



data1 = HighThcProducts(products, products_df).getData()


htc = HighThcCompanies(products, products_df)
htc_data = htc.getData()
htc_img = htc.getImage(htc_data)


hvc = HighValueCompanies(products, products_df)
hvc_data = hvc.getData()
hvc_img = hvc.getImage(hvc_data)




