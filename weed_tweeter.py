# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:53:41 2020

@author: Jarrett
"""

import subprocess
import json
import pandas as pd


def get_min_max_as_percent(text):
    # has to be either % or mg/g 
    data = {
        'min': 0,
        'max': 0
    }
    
    if '<' in text:
        # some small number, return zero
        pass
    
    elif '%' in text:
        text = text.replace('%', '')
        text = text.strip()
        split_text = text.split('−')
        
        if len(split_text) == 2:
            data['min'] = float(split_text[0])
            data['max'] = float(split_text[1])
        else:
            data['min'] = float(split_text[0])
            data['max'] = float(split_text[0])
    elif 'mg/g' in text:
        text = text.replace('mg/g', '')
        text = text.strip()
        split_text = text.split('−')
        
        if len(split_text) == 2:
            data['min'] = float(split_text[0]) / 10
            data['max'] = float(split_text[1]) / 10
        else:
            data['min'] = float(split_text[0]) / 10
            data['max'] = float(split_text[0]) / 10
    else:
        # must just be a single digit?
        text = text.strip()
        if len(text) == 1:
            text = float(text)
            data['min'] = text
            data['max'] = text
    
    data['avg'] = (data['min'] + data['max']) / 2
    
    return data

  
def get_price_as_float(price_text):
        price_text = price_text.replace('CAD', '')
        price_text = price_text.replace('$', '')
        price_text = price_text.strip()
        price = float(price_text)
        return price


# add the parsed thc and cbd data to the product, as its original as a string
# other data cleaning
def update_products(products):
    for product in products:
        thc_data = get_min_max_as_percent(product['Thc'])
        product['thc_min'] = thc_data['min']
        product['thc_max'] = thc_data['max']
        product['thc_avg'] = thc_data['avg']
        cbd_data = get_min_max_as_percent(product['Cbd'])
        product['cbd_min'] = cbd_data['min']
        product['cbd_max'] = cbd_data['max']
        product['cbd_avg'] = cbd_data['avg']
        
        product['adjusted_price_float'] = get_price_as_float(product['AdjustedPrice'])
        product['list_price_float'] = -1
        
        if product['ListPrice'] is not None:
            product['list_price_float'] = get_price_as_float(product['ListPrice'])
            
        product['dollar_per_gram'] = product['adjusted_price_float'] / float(product['Quantity'])
        product['dollar_per_mg_thc'] = product['adjusted_price_float'] / (float(product['Quantity']) * product['thc_avg'])
    
    return (products, pd.DataFrame(products))



abc = subprocess.run('curl "https://www.albertacannabis.org/api/cxa/CatalogExtended/GetProductList" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0" -H "Accept: */*" -H "Accept-Language: en-CA,en-US;q=0.7,en;q=0.3" -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" -H "__RequestVerificationToken: OUp10VUDi8VBEpbeVk7VD7HT1JWlmWnNbwp_FQcxTqr4aR28Mwkk2mNnjMk1Og-GhmVOgnX3wdyYMCoRo5_auLhukJo1" -H "X-Requested-With: XMLHttpRequest" -H "Origin: https://www.albertacannabis.org" -H "DNT: 1" -H "Connection: keep-alive" -H "Referer: https://www.albertacannabis.org/shop/Cannabis=aglc_cannabis-cannabis?f=format"%"3DDried"%"20Flower|Milled"%"20Flower&ps=400" -H "Cookie: f5_cspm=1234; ASP.NET_SessionId=h20zueiku1f1fwxnuxu1jgnn; SC_ANALYTICS_GLOBAL_COOKIE=7856d2e38a9d4c38b9b918028f090ab1|True; __RequestVerificationToken=FZhJ866Bt00z0vp_qcULMngZ8JPxJBCx5XUBP39NR2Ho3Isj9iRgtZHF78DUVWTTaQxSQrtPsD4Ng4ax5R2gMXsb6eg1; sxa_site=Cannabis; f5avr1519412710aaaaaaaaaaaaaaaa=BGPDFPBELJOLKMEEKEGFHKKEOKNHMBBFCLMEINGDELJNEDDMEDHGBIHHEMNKJGDDLCNPCPDGOCMCKFBMMLIDFCIJOHMAICDNJNMCKDGPKCJFKONJAFEHFKOJMKDCAJBA" --data-raw "pg=0&f=format"%"253DDried"%"2520Flower"%"7CMilled"%"2520Flower&ps=400&sd=Asc&cci="%"7BDAAC337F-EC42-9DD5-33BC-851875C99BEB"%"7D&ci="%"7BC8173B3F-26C8-41AB-B042-9CAAD37B543B"%"7D&__RequestVerificationToken=OUp10VUDi8VBEpbeVk7VD7HT1JWlmWnNbwp_FQcxTqr4aR28Mwkk2mNnjMk1Og-GhmVOgnX3wdyYMCoRo5_auLhukJo1"', 
                     shell=True, check=True, capture_output=True, encoding='utf-8')


canna_json = json.loads(abc.stdout)

products, products_df = update_products(canna_json['Variants'])

cbd_types = { p['Cbd'] for p in products }
thc_types = { p['Thc'] for p in products }

cbd_percents = [(c, get_min_max_as_percent(c)) for c in cbd_types]
thc_percents = [(t, get_min_max_as_percent(t)) for t in thc_types]


# based on thc or cbd percentage
max_thc = sorted(products, key=lambda p: p['thc_max'], reverse=True)
max_cbd = sorted(products, key=lambda p: p['cbd_max'], reverse=True)
min_thc = sorted(products, key=lambda p: p['thc_min'] + p['thc_avg'], reverse=True)
mix_super_thc = sorted(products, key=lambda p: (p['thc_min'] + p['thc_avg']) - (p['thc_max'] - p['thc_min']), reverse=True)
min_thc = sorted(products, key=lambda p: p['thc_min'], reverse=True)



# find best dollars per gram
dollar_per_gram = sorted(products, key=lambda p: p['dollar_per_gram'])


# dollar per milligram of thc  (use the average thc?)
dollar_per_mg_thc = sorted(products, key=lambda p: p['dollar_per_mg_thc'])


# cheapest form factor overall



# cheapest brands
# get the brand names
brand_names = {p['Brand'] for p in products}

# summarize by brand


# most expensive brands



# price drops



# market averages
# 1g
one_gram_products = list(filter(lambda p: p['Quantity'] == '1', products))
one_gram_df = pd.DataFrame(one_gram_products)
one_gram_desc = one_gram_df.describe()

# 3.5g
threepointfive_gram_products = list(filter(lambda p: p['Quantity'] == '3.5', products))
threepointfive_gram_df = pd.DataFrame(threepointfive_gram_products)
threepointfive_gram_desc = threepointfive_gram_df.describe()

# mid
seven_gram_products = list(filter(lambda p: p['Quantity'] == '5' or p['Quantity'] == '7', products))
seven_gram_df = pd.DataFrame(seven_gram_products)
seven_gram_desc = seven_gram_df.describe()

# mid-large format 14 and 15
midformat_products = list(filter(lambda p: p['Quantity'] == '14' or p['Quantity'] == '15', products))
midformat_df = pd.DataFrame(midformat_products)
midformat_desc = midformat_df.describe()

# large format 21 an 28
largeformat_products = list(filter(lambda p: p['Quantity'] == '21' or p['Quantity'] == '28', products))
largeformat_df = pd.DataFrame(largeformat_products)
largeformat_desc = largeformat_df.describe()



# graphs!  generate some graphs

# histogram of average dollars per gram by product weight







# other cool things