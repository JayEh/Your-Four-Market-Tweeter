# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:17:18 2020

@author: j
"""

from scipy.special import softmax
import matplotlib.pyplot as plt
import numpy as np
import locale
import pandas as pd
from datetime import date

locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8') # used for formatting currency
plt.style.use('dark_background') # used for the visual style of the plots


# inherit this class
class TweetCard():
    def __init__(self, products=None, products_df=None, rows=None, figsize=None, filename=None):
        self.products = products
        self.products_df = products_df
        self.rows = rows
        self.figsize = figsize
        self.y_font_size = 12
        self.filename = f'.\\generated\\{filename}.png'
        self.hashtags = ['#alberta', '#abcannabis', '#canadiancannabis', '#yyccannabis', '#yegcannabis', '#canadianweed ']
        


class GovernmentURLs(TweetCard):
    def getData(self):
        # the top link is basically a root page for the others 
        # https://www.canada.ca/en/health-canada/services/drugs-medication/cannabis.html
        # https://www150.statcan.gc.ca/n1/pub/13-610-x/13-610-x2018001-eng.htm
        # https://www.canada.ca/en/health-canada/services/publications/drugs-health-products/canadian-cannabis-survey-2019-summary.html
        # https://surveys-enquetes.statcan.gc.ca/cannabis/
        return None
    
    
    def getImage(self, data):
        return None
    
    
    def getTweetText(self):
        hashtags = ' '.join(self.hashtags)
        text = (
            'This is the Alberta Bud Report. Remember! Stay informed and use cannabis responsibly. \n'
            'https://www.canada.ca/en/health-canada/services/drugs-medication/cannabis.html \n'
            f'{hashtags}'
            )
        return text
    

class TopDollarProducts(TweetCard):
    def getData(self):
        rows = self.rows
        
        pdf = self.products_df[self.products_df['Quantity'] == '3.5']
        
        # calculate the mean + 1std for thc_max, select out those rows
        df_mean = pdf['adjusted_price_float'].mean()
        df_std = pdf['adjusted_price_float'].std()
        
        report_rows = pdf.groupby(['Brand']).mean()
        report_rows = report_rows[report_rows['adjusted_price_float'] >= df_mean + df_std]
        report_rows = report_rows.reset_index()
        row_probs = softmax(report_rows['adjusted_price_float'].tolist())
        
        # select however many to put in the report (randomly)
        rows = min(rows, len(report_rows))
        self.actual_rows = rows
        row_idxs = np.arange(len(report_rows))
        additional_rows_idxs = np.random.choice(row_idxs, p=row_probs, size=rows, replace=False).tolist()
        
        # select the additional rows by index
        report_rows = report_rows.iloc[additional_rows_idxs]
                
        # bring the data together
        top_brands = report_rows['Brand'].tolist()
        top_prices = list((report_rows['adjusted_price_float']).values)
        data =  list(zip(top_brands, top_prices))
        
        # add the market average
        data = sorted(data, key=lambda x: x[1], reverse=False)
        data.insert(len(data), ('Market Average (3.5g only)', round(df_mean, 1)))
        return data
    
    
    def getImage(self, data):
        fig, ax = plt.subplots(figsize=self.figsize)
        
        companies = [d[0] for d in data]
        top_prices = [d[1] for d in data]
        y_pos = np.arange(len(companies))
        
        for i, price in enumerate(top_prices):
            average_price = locale.currency(top_prices[i]) + ' / 3.5g'
            ax.text(1.0, i, average_price, verticalalignment='center', color='white', fontsize=12)
        
        
        bar_colors = [(75/256,75/256,75/256) for _ in range(len(data))]
        bar_colors[len(bar_colors)-1] = (30/256,30/256,30/256)
        
        ax.barh(y_pos, top_prices, align='center', color=bar_colors)
        ax.set_ylabel('Brand', fontsize=self.y_font_size)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies, fontsize=self.y_font_size)
        
        formatted_date = date.today().strftime('%B %d, %Y')
        ax.set_xlabel(f'From AlbertaCannabis.org on {formatted_date}')
        
        ax.set_xticks([])
        ax.set_title((
            'Alberta Bud Report \n'
            'Top Dollar Eighths (3.5g) Average Selling Price \n'
            f'{formatted_date}'))
        plt.savefig(self.filename, bbox_inches='tight')
        plt.show()
        
        
    def getTweetText(self):
        text = (
            f'The Alberta Bud Report. Here are {self.actual_rows} brands charging top dollar for their products.'
            )
        return text


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
        ax.set_ylabel('Brand', fontsize=self.y_font_size)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_brands, fontsize=self.y_font_size)
        ax.invert_yaxis()  # sort desc
        
        for i,d in enumerate(data):
            formatted_amount = locale.currency(d[1]) + ' / gram'
            ax.text(0.25, i, formatted_amount, verticalalignment='center', color='white')
        
        
        ax.xaxis.set_visible(False)
        ax.set_title('AGLC - Lowest Average Dollar Per Gram by Brand')
        plt.show()
        
        plt.savefig('my_figure.png', bbox_inches='tight')
        # save the figure
        # return it?


class HighValueProducts(TweetCard):
    def getData(self):
        rows = self.rows
        
        # calculate the mean + 1std for thc_max, select out those rows
        df_mean = self.products_df['dollar_per_gram'].mean()
        df_std = self.products_df['dollar_per_gram'].std()
        
        report_rows = self.products_df.groupby(['Brand','DisplayName']).mean()
        report_rows = report_rows[report_rows['dollar_per_gram'] <= df_mean - df_std]
        report_rows = report_rows.reset_index()
        row_idxs = np.arange(len(report_rows)) 
        reversed_rows = report_rows['dollar_per_gram'] * -1 
        row_probs = softmax(reversed_rows.tolist())
        
        rows = min(rows, len(report_rows))
        self.actual_rows = rows
        
        # select however many to put in the report (randomly)
        additional_rows_idxs = np.random.choice(row_idxs, p=row_probs, size=rows, replace=False).tolist()
        
        # select the additional rows by index
        report_rows = report_rows.iloc[additional_rows_idxs]
        
        # what quantities can you buy this in?      
        quantities = []
        prices = []
        for brand, product in zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()):
            pdf = self.products_df
            filtered_df = pdf[(pdf['Brand'] == brand) & (pdf['DisplayName'] == product)]
            jar_sizes = filtered_df['Quantity'].unique().tolist()
            price_range = filtered_df['adjusted_price_float'].unique().tolist()
            quantities.append(jar_sizes)
            prices.append(price_range)
        
        # bring the data together
        top_brands = list(zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()))
        top_dpg = list((report_rows['dollar_per_gram']).values)
        data =  list(zip(top_brands, top_dpg, quantities, prices))
        
        # add the market average
        data = sorted(data, key=lambda x: x[1], reverse=True)
        data.insert(len(data), (('Market Average',''), round(df_mean, 1), [], []))
        return data
        
    
    def getImage(self, data):
        fig, ax = plt.subplots(figsize=self.figsize)
        
        companies_and_products = [d[0] for d in data]
        avg_dpg = [d[1] for d in data]
        quantities = [d[2] for d in data]
        prices = [d[3] for d in data]
        companies = [c[0] for c in companies_and_products]
        products = [c[1] for c in companies_and_products]
        
        y_pos = np.arange(len(companies_and_products))
        
        for i,product_name in enumerate(products):
            # add text for quantities and prices
            text_items = [] # join the elements in this list once they are all collected
            bar_text = product_name

            for qi, pi in list(zip(quantities[i], prices[i])):
                q = f'{qi}g'

                #p = locale.currency(pi) # this is troublesome since $ is a special character for plt
                p = f'\${pi}'

                t = f'{q} / {p}'
                text_items.append(t)

                if len(text_items) > 0:
                    product_text = ',  '.join(text_items)
                    bar_text = f'{product_name}   ({product_text})'
                else:
                    bar_text = f'{product_name}'

            
            if i == len(products)-1: 
                dollars_per_gram = locale.currency(avg_dpg[i]) + ' / gram'
                t_color = 'white' 
            else: 
                dollars_per_gram = ''
                t_color = 'black'
            
            ax.text(0.25, i, bar_text, verticalalignment='center', color='white')
            ax.text(0.25, i, dollars_per_gram, verticalalignment='center', color=t_color, fontsize=12)
            
        
        bar_colors = [(75/256,75/256,75/256) for _ in range(len(data))]
        bar_colors[len(bar_colors)-1] = (30/256,30/256,30/256)
        
        ax.barh(y_pos, avg_dpg, align='center', color=bar_colors)
        ax.set_ylabel('Brand', fontsize=self.y_font_size)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies, fontsize=self.y_font_size)
        
        formatted_date = date.today().strftime('%B %d, %Y')
        ax.set_xlabel(f'From AlbertaCannabis.org on {formatted_date}')
        
        ax.set_xticks([])
        ax.set_title((
            'Alberta Bud Report \n'
            'Lowest $ / gram (and available quantities) \n'
            f'{formatted_date}'
            ))
        plt.savefig(self.filename, bbox_inches='tight')
        plt.show()

    def getTweetText(self):
        text = (
            f'The Alberta Bud Report. These {self.actual_rows} products are a selection of the lowest dollar per gram on the market today. '
            'Check back daily for an updated report!'
            )
        
        return text


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
        row_probs = softmax(report_rows['thc_max'].tolist())
        
        rows = min(rows, len(report_rows))
        self.actual_rows = rows
        
        # select however many to put in the report (randomly)
        additional_rows_idxs = np.random.choice(row_idxs, p=row_probs, size=rows, replace=False).tolist()
        
        # select the additional rows by index
        report_rows = report_rows.iloc[additional_rows_idxs]
        
        # what quantities can you buy this in?
        quantities = []
        prices = []
        for brand, product in zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()):
            pdf = self.products_df
            filtered_df = pdf[(pdf['Brand'] == brand) & (pdf['DisplayName'] == product)]
            jar_sizes = filtered_df['Quantity'].unique().tolist()
            price_range = filtered_df['adjusted_price_float'].unique().tolist()
            quantities.append(jar_sizes)
            prices.append(price_range)
            
        
        # bring the data together
        top_brands = list(zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()))
        top_thc = list((report_rows['thc_max']).values)
        data =  list(zip(top_brands, top_thc, quantities, prices))
        
        # add the market average
        data = sorted(data, key=lambda x: x[1])
        data.insert(len(data), (('Market Average',''), round(df_mean, 1), [], []))
        return data
    
    
    def getImage(self, data):
        fig, ax = plt.subplots(figsize=self.figsize)
        
        companies_and_products = [d[0] for d in data]
        avg_thc = [d[1] for d in data]
        quantities = [d[2] for d in data]
        prices = [d[3] for d in data]
        companies = [c[0] for c in companies_and_products]
        products = [c[1] for c in companies_and_products]
        
        y_pos = np.arange(len(companies_and_products))
        
        for i,product_name in enumerate(products):
            # add text for quantities and prices
            text_items = [] # join the elements in this list once they are all collected
            for qi, pi in list(zip(quantities[i], prices[i])):
                q = f'{qi}g'
                
                #p = locale.currency(pi) # this is troublesome since $ is a special character for plt
                p = f'\${pi}'
                
                t = f'{q} / {p}'
                text_items.append(t)
            
            if len(text_items) > 0:
                product_text = ',  '.join(text_items)
                bar_text = f'{product_name}   ({product_text})'
            else:
                bar_text = f'{product_name}'
            
            # set the text for bar i
            plt.text(1.0, i, bar_text, verticalalignment='center', color='white')
        
        bar_colors = [(0.35+(i/(len(data) *3)),0,0) for i in range(len(data))]
        bar_colors[len(bar_colors)-1] = (30/256,30/256,30/256)
        
        ax.barh(y_pos, avg_thc, align='center', color=bar_colors)
        ax.set_ylabel('Brand', fontsize=self.y_font_size)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies, fontsize=self.y_font_size)
                
        formatted_date = date.today().strftime('%B %d, %Y')
        ax.set_xlabel(f'From AlbertaCannabis.org on {formatted_date}')
        
        ax.set_xticks([])
        ax.set_title((
            'Alberta Bud Report \n'
            'Above Average THC % (and available quantities) \n'
            f'{formatted_date}'
            ))
        plt.savefig(self.filename, bbox_inches='tight')
        plt.show()
        
        
    def getTweetText(self):
        tweet_text = (
            f'The Alberta Bud Report. Here are {self.actual_rows} of the most potent products on the market. '
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
        report_rows['pure_cbd'] = report_rows['thc_min'].lt(1.0)
        
        self.pure_cbd_count =  report_rows['pure_cbd'].sum()
        self.blend_count = len(report_rows['pure_cbd']) - report_rows['pure_cbd'].sum()
        
        # what quantities can you buy this in?
        quantities = []
        prices = []
        for brand, product in zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()):
            pdf = self.products_df
            filtered_df = pdf[(pdf['Brand'] == brand) & (pdf['DisplayName'] == product)]
            jar_sizes = filtered_df['Quantity'].unique().tolist()
            price_range = filtered_df['adjusted_price_float'].unique().tolist()
            quantities.append(jar_sizes)
            prices.append(price_range)
            
        # bring the data together
        top_brands = list(zip(report_rows['Brand'].tolist(), report_rows['DisplayName'].tolist()))
        top_cbd = report_rows['cbd_avg'].tolist()
        pure_cbd = report_rows['pure_cbd'].tolist()
        
        data = list(zip(top_brands, top_cbd, quantities, pure_cbd, prices))
        data = sorted(data, key=lambda x: x[1], reverse=False)
        return data
    
    def getImage(self, data):
        fig, ax = plt.subplots(figsize=self.figsize)
        
        companies_and_products = [d[0] for d in data]
        avg_cbd = [d[1] for d in data]
        quantities = [d[2] for d in data]
        pure_cbd = [d[3] for d in data]
        prices = [d[4] for d in data]
        
        companies = [c[0] for c in companies_and_products]
        products = [c[1] for c in companies_and_products]
        
        y_pos = np.arange(len(companies_and_products))
        
        for i, product_name in enumerate(products):            
            text_items = []
            for qi, pi in list(zip(quantities[i], prices[i])):
                q = f'{qi}g'
                
                #p = locale.currency(pi) # this is troublesome since $ is a special character for plt
                p = f'\${pi}'
                
                t = f'{q} / {p}'
                text_items.append(t)

            if len(text_items) > 0:
                product_text = ',  '.join(text_items)
                bar_text = f'{product_name}   ({product_text})'
            else:
                bar_text = f'{product_name}'
            
            # bar_text = product_name
            # if len(quantities[i]) > 0:
            #     q = [str(q)+'g' for q in quantities[i]]
            #     q = ', '.join(q)
            #     q = f'   ({q})'
            #    bar_text += q
            
            ax.text(0.5, i, bar_text, verticalalignment='center', color='white')
        
        
        green = (10/256,75/256,10/256)
        blue = (0/256,120/256,120/256)
        lookup = {
            True: blue,
            False: green
            }
        
        bar_colors = [lookup[d] for d in pure_cbd]
        
        ax.barh(y_pos, avg_cbd, align='center', color=bar_colors)
        ax.set_ylabel('Brand', fontsize=self.y_font_size)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies, fontsize=self.y_font_size)
        
        # how do I set the font to make it easier to read?
        
        formatted_date = date.today().strftime('%B %d, %Y')
        ax.set_xlabel(f'From AlbertaCannabis.org on {formatted_date}')
        
        ax.set_xticks([])
        ax.set_title((
            'Alberta Bud Report \n'
            'CBD (blue) and CBD/THC (green) (and available quantities) \n'
            f'{formatted_date}'
            ))
        plt.savefig(self.filename, bbox_inches='tight')
        plt.show()

    def getTweetText(self):
        tweet_text = (            
            f'The Alberta Bud Report. Check out these {self.pure_cbd_count} CBD products and another {self.blend_count} with a THC/CBD blend. '
            'The Alberta market has relatively low selection of CBD products.'
            )
        
        return tweet_text



