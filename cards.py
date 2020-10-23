# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:17:18 2020

@author: jarre
"""

import matplotlib.pyplot as plt
import numpy as np
import locale
import pandas as pd
from datetime import date

locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')
plt.style.use('ggplot')


# inherit this class
class TweetCard():
    def __init__(self, products, products_df, rows, figsize):
        self.products = products
        self.products_df = products_df
        self.rows = rows
        self.figsize = figsize


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
    
    def getData(self):
        rows = self.rows
        
        # calculate the mean + 1std for thc_max, select out those rows
        df_mean = self.products_df['thc_max'].mean()
        df_std = self.products_df['thc_max'].std()
        
        report_rows = self.products_df.groupby(['Brand','DisplayName']).mean()
        report_rows = report_rows[report_rows['thc_max'] >= df_mean + df_std]
        report_rows = report_rows.reset_index()
        row_idxs = np.arange(len(report_rows))
        row_probs = np.full(len(report_rows), 1/len(report_rows))
        
        # select however many to put in the report (randomly)
        additional_rows_idxs = np.random.choice(row_idxs, p=row_probs, size=rows, replace=False).tolist()
        
        # select the additional rows by index
        report_rows = report_rows.iloc[additional_rows_idxs]
        
        # what quantities can you buy this in?      
        quantities = []
        for brand, product in zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()):
            pdf = self.products_df
            filtered_df = pdf[(pdf['Brand'] == brand) & (pdf['DisplayName'] == product)]
            jar_sizes = filtered_df['Quantity'].tolist()
            quantities.append(jar_sizes)
        
        # bring the data together
        top_brands = list(zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()))
        top_thc = list((report_rows['thc_max']).values)
        data =  list(zip(top_brands, top_thc, quantities))
        
        # add the market average
        data = sorted(data, key=lambda x: x[1])
        data.insert(len(data), (('Market Average',''), round(df_mean, 1), []))
        
        return data
    
    
    def getImage(self, data):
        fig, ax = plt.subplots(figsize=self.figsize)
        
        companies_and_products = [d[0] for d in data]
        avg_thc = [d[1] for d in data]
        quantities = [d[2] for d in data]        
        companies = [c[0] for c in companies_and_products]
        products = [c[1] for c in companies_and_products]
        
        y_pos = np.arange(len(companies_and_products))
        
        for i,product_name in enumerate(products):
            bar_text = product_name
            if len(quantities[i]) > 0:
                q = [str(q)+'g' for q in quantities[i]]
                q = ', '.join(q)
                q = f'   ({q})'
                bar_text += q
            
            ax.text(0.5, i, bar_text, verticalalignment='center', color='white')
        
        bar_colors = [(0.35+(i/(len(data) *3)),0,0) for i in range(len(data))]
        bar_colors[len(bar_colors)-1] = (0.0,0,0)
        ax.barh(y_pos, avg_thc, align='center', color=bar_colors)
        ax.set_ylabel('Brand')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies)
        
        # how do I set the font to make it easier to read?
        
        formatted_date = date.today().strftime('%B %d, %Y')
        ax.set_xlabel(f'From AlbertaCannabis.org on {formatted_date}')
        
        ax.set_xticks([])
        ax.set_title('Flower - Above Average THC % (and available quantities)')
        plt.show()
        
        
    def getTweetText(self):
        # can use the df data here to help make the text that goes with
        # the image! 
        
        tweet_text = (
            f'Here are {self.rows} of the highest THC strains on the market. '
            f'Check back daily for a different {self.rows}.'
            )
        
        return tweet_text



class HighCbdProducts(TweetCard):
    def getData(self):        
        rows = self.rows
        
        # if there's not 1% cbd... exclude
        df = self.products_df[self.products_df['cbd_min'] > 1.0]
        
        report_rows = df.groupby(['Brand','DisplayName']).mean()
        report_rows = report_rows.reset_index()
        
        # try to take the max, but go with less if needed
        report_row_len = min(len(report_rows), rows)
        row_idxs = np.arange(report_row_len)
        row_probs = np.full(report_row_len, 1/report_row_len)
        
        # select however many to put in the report (randomly)
        additional_rows_idxs = np.random.choice(row_idxs, p=row_probs, size=report_row_len, replace=False).tolist()
        
        # select the additional rows by index
        report_rows = report_rows.iloc[additional_rows_idxs]
            
        # separate into pure CBD (min THC% < 1%) and blend (min THC% > 1%)
        cbd_rows = report_rows[report_rows['thc_min'] <= 1.0]
        blend_rows = report_rows[report_rows[thc_min] > 1.0]
        # JL TODO - resume here!
        
        
        # what quantities can you buy this in?      
        quantities = []
        for brand, product in zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()):
            pdf = self.products_df
            filtered_df = pdf[(pdf['Brand'] == brand) & (pdf['DisplayName'] == product)]
            jar_sizes = filtered_df['Quantity'].tolist()
            quantities.append(jar_sizes)
            
        
            
            
        
        # bring the data together
        top_brands = list(zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()))
        top_cbd = list((report_rows['cbd_avg']).values)
        
        
        data =  list(zip(top_brands, top_cbd, quantities))
        
        data = sorted(data, key=lambda x: x[1], reverse=True)
        return data
    
    def getImage(self, data):
        pass

    def getTweetText(self):
        pass







