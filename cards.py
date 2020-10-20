# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:17:18 2020

@author: jarre
"""

import matplotlib.pyplot as plt
import numpy as np
import locale
import pandas as pd
locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')
plt.style.use('ggplot')


# inherit this class
class TweetCard():
    def __init__(self, products, products_df):
        self.products = products
        self.products_df = products_df


class GovernmentURLs(TweetCard):
    def getData(self):
        # https://www.canada.ca/en/health-canada/services/drugs-medication/cannabis.html
        # https://www150.statcan.gc.ca/n1/pub/13-610-x/13-610-x2018001-eng.htm
        # https://www.canada.ca/en/health-canada/services/publications/drugs-health-products/canadian-cannabis-survey-2019-summary.html
        # https://surveys-enquetes.statcan.gc.ca/cannabis/
        
        pass
    
    
    def getImage(self):
        pass
    

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
        ax.set_title('AGLC - Highest Average THC Content by Brand')
        ax.set_ylabel('Brand')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies)
        ax.invert_yaxis()  # sort desc
        
        ax.set_xticks([])
        ax.set_xlabel('Data collected from AlbertaCannabis.org on {the date}')
        
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
        
        for i,d in enumerate(data):
            formatted_amount = locale.currency(d[1]) + ' / gram'
            ax.text(0.25, i, formatted_amount, verticalalignment='center', color='white')
        
        
        ax.xaxis.set_visible(False)
        ax.set_title('AGLC - Lowest Average Dollar Per Gram by Brand')
        plt.show()
        
        # save the figure
        # return it?


class HighValueProducts(TweetCard):
    def getData(self):
        pass
    
    def getImage(self):
        pass



class HighThcProducts(TweetCard):
    """
    Which companies have the highest THC products, and what are those products?
    """
    
    def getData_old(self):
        # this one is a little different... lots of people will be at like 27-28% and 
        # to be fair we should randomly select from that pool so everyone gets a chance
        
        rows = 10
        
        highest_thc = self.products_df.groupby(['Brand','DisplayName']).mean()
        highest_thc = highest_thc.sort_values(by=['thc_max', 'thc_min'], ascending=False)
        
        # these rows could be in the report. what is the lowest thc in the list?
        min_val = highest_thc['thc_max'][:rows].min()
        
        # take from highest THC where greater than min val, want those all the time
        # this could conceivably return 0 if all top rows have the same max
        report_rows = highest_thc[highest_thc['thc_max'] > min_val][:rows]
        
        # filter highest_thc on the min_val, use these to fill in the available report rows
        min_rows = highest_thc[highest_thc['thc_max'] == min_val][:rows]
        min_rows_idx = np.arange(len(min_rows))
        min_rows_prob = np.full(len(min_rows), 1/len(min_rows))
        
        # make a random selection from the available rows
        additional_rows_idxs = np.random.choice(min_rows_idx, p=min_rows_prob, size=rows-len(report_rows))
        
        # add the additional rows based on the random indexes in additional_rows_idx
        for idx in additional_rows_idxs:
            report_rows = report_rows.append(min_rows[idx:idx+1:])
        
        report_rows = report_rows.sort_values(by=['thc_max', 'thc_min'], ascending=False)
        
        
        quantities = []
        for brand, product in report_rows.index:
            pdf = self.products_df
            filtered_df = pdf[(pdf['Brand'] == brand) & (pdf['DisplayName'] == product)]
            jar_sizes = filtered_df['Quantity'].tolist()
            quantities.append(jar_sizes)
        
        
        # do this once all the products are selected in the special way
        top_brands = list(report_rows.index)
        top_thc = list((report_rows['thc_max']).values)
        return list(zip(top_brands, top_thc, quantities))
    
    
    def getData(self):
        rows = 15
        
        # calculate the mean + 1std for thc_max, select out those rows
        df_mean = self.products_df['thc_max'].mean()
        df_std = self.products_df['thc_max'].std()
        
        report_rows = self.products_df[self.products_df['thc_max'] >= df_mean + df_std]
        report_rows = report_rows.reset_index()
        row_idxs = np.arange(len(report_rows))
        row_probs = np.full(len(report_rows), 1/len(report_rows))
        
        # select however many to put in the report (randomly)
        additional_rows_idxs = np.random.choice(row_idxs, p=row_probs, size=rows).tolist()
        
        # something like this should work...? just select out the rows that were randomly selected
        report_rows = report_rows.iloc[additional_rows_idxs]
        
        # also calculate the market mean and add it as a comparison point
        
        
        quantities = []
        for brand, product in zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].list()):
            pdf = self.products_df
            filtered_df = pdf[(pdf['Brand'] == brand) & (pdf['DisplayName'] == product)]
            jar_sizes = filtered_df['Quantity'].tolist()
            quantities.append(jar_sizes)
        
        
        top_brands = list(report_rows.index)
        top_thc = list((report_rows['thc_max']).values)
        return list(zip(top_brands, top_thc, quantities))
    
    
    def getImage(self, data):
        fig, ax = plt.subplots()

        
        companies_and_products = [d[0] for d in data] # y axis
        avg_thc = [d[1] for d in data]   # x axis
        
        companies = [c[0] for c in companies_and_products]
        products = [c[1] for c in companies_and_products]
        y_pos = np.arange(len(companies_and_products))
        
        for i,product_name in enumerate(products):
            ax.text(0.5, i, product_name, verticalalignment='center', color='white')
        
        ax.barh(y_pos, avg_thc, align='center')
        ax.set_ylabel('Brand')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies)        
        ax.invert_yaxis()  # sort desc
        
        ax.set_xticks([])
        ax.set_title('High Average THC Content')
        plt.show()




# data1 = HighThcProducts(products, products_df).getData()


# hvc = HighValueCompanies(products, products_df)
# hvc_data = hvc.getData()
# hvc_img = hvc.getImage(hvc_data)


# htc = HighThcCompanies(products, products_df)
# htc_data = htc.getData()
# htc_img = htc.getImage(htc_data)






