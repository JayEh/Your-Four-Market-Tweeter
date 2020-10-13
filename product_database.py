# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 12:31:38 2020

@author: jarre
"""

# use sqlite to collect market data

import sqlite3
import os

DB_ROOT = 'C:\\Python\\Cannabrain\\yf1'
APP_DB = os.path.join(DB_ROOT, 'app_db.db')


# hacky because it connects and drops at each sql statement!
def hacky_run_sql(sql_string, params=None):
    sqlConnection = sqlite3.connect(APP_DB)
    c = sqlConnection.cursor()
    
    if (params is None):
        c.execute(sql_string)
    else:
        c.execute(sql_string, params)

    # if the statement was not an insert this will be zero
    c.execute ('select last_insert_rowid()')
    last_id = c.fetchone()
    
    sqlConnection.commit()    
    sqlConnection.close()
    
    return last_id


# hacky because it connects and drops at each sql statement!
def hacky_select_sql(sql_string, params=None):
    sqlConnection = sqlite3.connect(APP_DB)
    c = sqlConnection.cursor()
    
    if (params is None):
        c.execute(sql_string)
    else:
        c.execute(sql_string, params)

    results = c.fetchall()
    
    sqlConnection.commit()
    sqlConnection.close()
    
    return results


# each product gets a SQL statement for insert
def saveProductsToDb(products):
    col_names = [col for col in products[0].keys()]
    col_param_placeholders = ','.join(['?' for col in products[0].keys()])
    inserted_ids = []
    
    for p in products:
        col_params = [str(p[col]) for col in col_names]
        col_names_string = ','.join(col for col in col_names)
        
        insert_sql = f'INSERT INTO product_history ({col_names_string}) VALUES ({col_param_placeholders})'
        inserted_id = hacky_run_sql(insert_sql, col_params)
        inserted_ids.append(inserted_id)
    
    return inserted_ids


# inserted_ids = saveProductsToDb(products)


