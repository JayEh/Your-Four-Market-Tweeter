# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:17:18 2020

@author: jarre
"""

import matplotlib.pyplot as plt


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
        min_thc_sorted = sorted(self.products, key=lambda p: p['thc_avg'], reverse=True)
        products_to_report = 10
        counter = 0
        companies = set()
        
        while len(companies) < products_to_report and counter < len(self.products):
            product = min_thc_sorted[counter]
            companies.add((product['Brand'], product['DisplayName'], product['thc_avg']))
            counter += 1
        
        companies = sorted(list(companies), key=lambda p:p[2], reverse=True)
        return companies
    
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

        # sample code from online, adapt it!
        # Example data
        companies = [d[0] for d in data]
        
        y_pos = np.arange(len(companies))
        
        performance = 3 + 10 * np.random.rand(len(people))
        
        
        ax.barh(y_pos, performance, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(companies)
        
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Brands')
        ax.set_title('Brands with highest average THC content.')
        
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
    
    def getImage(self):
        pass




data1 = HighThcProducts(products, products_df).getData()


htc = HighThcCompanies(products, products_df)
htc_data = htc.getData()
htc_img = htc.getImage(htc_data)


data3 = HighValueCompanies(products, products_df).getData()





