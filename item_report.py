# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 01:50:09 2016

@author: Gerard
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

inv_tran = pd.read_csv('inv_tran.csv')
po_tran = pd.read_csv('po_tran.csv')
adj_tran = pd.read_csv('adj_tran.csv')
cycle_tran = pd.read_csv('cycle_tran.csv')
sales_tran = pd.read_csv('sales_tran.csv')

def basic_stats(item_num):
    #filters out item_num
    item_tran = sales_tran[sales_tran['ITEM_NUM'] == item_num]
    #calculate and prints mean and standard deviation - should turn to an object
    mean = item_tran['SALES'].mean()
    std= item_tran['SALES'].std() 
    print 'The average sale of the item is', mean
    print 'The standard deviation of the item is', std
    #plots daily use plots single purchases.
    item_tran['SALES'].hist(bins = 50)
    day_group = item_tran['SALES'].groupby(item_tran['INV_DATE'])
    by_day = day_group.agg(np.sum)    
    by_day.hist(bins = 50)
    daily_mean = by_day.mean()
    daily_std = by_day.std()
    print 'The average daily throughput is' , daily_mean
    print 'The daily throughput standard deviation is', daily_std
    cust_group = item_tran['SALES'].groupby(item_tran['CUST_NAME'])
    by_cust = cust_group.agg(np.sum).nlargest(5)
    sum_sales = item_tran['SALES'].sum()
    by_cust = pd.DataFrame(by_cust)
    by_cust['PERC_OF_ITEM'] = by_cust['SALES'].apply(lambda x: (x/sum_sales)*100)
    print by_cust
    return by_cust

#item = basic_stats('ATCS24AWH')

def basic_cycle(item_num):
    item_filter = cycle_tran['ITEM_NUM'] == item_num
    item_tran = cycle_tran[item_filter]
    day_group = item_tran['ADJUSTMENTS'].groupby(item_tran['INV_DATE']).agg(np.sum)
    
    return day_group

cycle = basic_cycle('02GASTP3CH')
print cycle.head(5)


'''
Put an upper function on item numbers and error handling when item doesn't exist.
Move prints to some sort of function - the variables are sent to a class.
Print Item Description at the top.
Plot of current stock next to sales.
Bins need to change depending on amount usually purchased (mean).
Simple report of last couple of cycles.
Import the correct types for each variable in the other module.
Need to figure out how to let the user select the file through Windows.
'''