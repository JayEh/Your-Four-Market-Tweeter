# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:31:38 2020

@author: j
"""

from datetime import datetime
import sqlite3
import os

DB_ROOT = 'C:\\Python\\Cannabrain\\yf1'
APP_DB = os.path.join(DB_ROOT, 'app_db.db')



def loadDbToDf():
    columns_list = ['id','adjusted_price_float','AdjustedPrice','Brand','Brand','Cbd',
               'cbd_avg','cbd_max','cbd_min','DisplayName','dollar_per_gram',
               'dollar_per_mg_thc','Format','ImageUrl','IsAuthenticated','IsCase',
               'IsInStock','Link','list_price_float','ListPrice','MasterCaseQuantity',
               'ProductId','Quantity','QuantityMeasure','SkuId','Strain','Thc',
               'thc_avg','thc_max','thc_min','Type','VariantId','date']
    
    columns_s = ','.join(columns_list)
    select_sql = f'select {columns_s} from product_history'
    


# load all the rows from the table and return a df
def loadTweetHistory():
    pass



# hacky because it connects and drops at each sql statement!
def hacky_run_sql(c, sqlConnection, sql_string, params=None):
    if (params is None):
        c.execute(sql_string)
    else:
        c.execute(sql_string, params)

    # if the statement was not an insert this will be zero
    c.execute ('select last_insert_rowid()')
    last_id = c.fetchone()
    
    return last_id


# hacky because it connects and drops at each sql statement!
def hacky_select_sql(c, sqlConnection, sql_string, params=None):
    if (params is None):
        c.execute(sql_string)
    else:
        c.execute(sql_string, params)

    results = c.fetchall()
    return results


# each product gets a SQL statement for insert
def saveProductsToDb(products):
    col_names = [col for col in products[0].keys()]
    col_param_placeholders = ','.join(['?' for col in products[0].keys()])
    inserted_ids = []
    
    sqlConnection = sqlite3.connect(APP_DB)
    c = sqlConnection.cursor()
    
    for p in products:
        col_params = [str(p[col]) for col in col_names]
        col_names_string = ','.join(col for col in col_names)
        insert_sql = f'INSERT INTO product_history ({col_names_string}) VALUES ({col_param_placeholders})'
        inserted_id = hacky_run_sql(c, sqlConnection, insert_sql, col_params)
        inserted_ids.append(inserted_id)
    
    sqlConnection.commit()
    sqlConnection.close()
    
    return inserted_ids


def hasTaskRunToday(task, date):
    sql = "SELECT * FROM tweet_history WHERE DATE(date)=DATE(?) AND card_type=(?)"
    date_where = f'{date.year}-{date.month}-{date.day}'
    params = [date_where, task['filename']]
    
    sqlConnection = sqlite3.connect(APP_DB)
    c = sqlConnection.cursor()
    results = hacky_select_sql(c, sqlConnection, sql, params)
    sqlConnection.close()
    
    # if the last returned id is 0 then it 
    return len(results) > 0
        

def saveTweetToHistory(tweet_response_json, category, card_type):
    """

    Parameters
    ----------
    tweet_response_json : TYPE
        DESCRIPTION.
    category : TYPE
        DESCRIPTION.
    card_type : TYPE
        DESCRIPTION.

    Returns
    -------
    inserted_id : TYPE
        DESCRIPTION.

    """
    
    col_names = ['response_json','category','card_type','date']
    col_names_string = ','.join(col_names)
    col_param_placeholders = ','.join(['?' for _ in range(len(col_names))])
    
    insert_sql = f'INSERT INTO tweet_history ({col_names_string}) VALUES ({col_param_placeholders})'
    col_params = [tweet_response_json, category, card_type, str(datetime.now())]
    
    sqlConnection = sqlite3.connect(APP_DB)
    c = sqlConnection.cursor()
    
    inserted_id = hacky_run_sql(c, sqlConnection, insert_sql, col_params)
    
    sqlConnection.commit()
    sqlConnection.close()
    
    return inserted_id


# inserted_ids = saveProductsToDb(products)


