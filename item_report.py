# -*- coding: utf-8 -*-


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


    
inv_tran = pd.read_csv('inv_tran.csv')
po_tran = pd.read_csv('po_tran.csv')
adj_tran = pd.read_csv('adj_tran.csv')
cycle_tran = pd.read_csv('cycle_tran.csv')
sales_tran = pd.read_csv('sales_tran.csv')
    
    
def basic_filter(item_num, csvfile):
    item_filter = csvfile['ITEM_NUM'] == item_num.upper()
    item_tran = csvfile[item_filter]
    return item_tran
    
def item_desc(item_sales):
    item_desc = item_sales.iloc[1]['ITEM_DESC']
    return item_desc
    
def basic_stats(series):
    mean = series.mean()
    std = series.std()
    basic_stats = {'mean':mean, 'std':std}
    return basic_stats

def plots(hist1, hist2, day_plot, month_plot):
    plt.figure()
    hist1.hist(bins = 50)
    plt.figure()
    hist2.hist(bins = 50)
    plt.figure()
    day_plot.plot()
    plt.figure()
    month_plot.plot()
    
def sales_info(item_num):
    item_sales = basic_filter(item_num, sales_tran)
    item_descr = item_desc(item_sales)
    sale_stats = basic_stats(item_sales['SALES'])
    day_sales = item_sales['SALES'].groupby(item_sales['INV_DATE']).agg(np.sum)
    day_stats = basic_stats(day_sales)
        
    #Groups sales by customer and takes the 5 largest. Gives percentage of total sales for those.
    cust_group = item_sales['SALES'].groupby(item_sales['CUST_NAME']).agg(np.sum).nlargest(5)
    cust_group = pd.DataFrame(cust_group)
    sum_sales = item_sales['SALES'].sum()
    cust_group['PERC_OF_ITEM'] = cust_group['SALES'].apply(lambda x: (x/sum_sales)*100)
    
    #Dictionary with all relevant information from sales_info.
    sales_data = {'sales_mean':sale_stats['mean'], 'sales_std': sale_stats['std'],
                  'day_mean':day_stats['mean'], 'day_std': day_stats['std'], 'top_5': cust_group,
                  'item_desc': item_descr, 'item_num':item_num}               
    return sales_data

def cycle_info(item_num):
    item_cycle = basic_filter(item_num, cycle_tran)
    #aggregating by day makes more sense, avoids same day errors in input.
    day_cycle = item_cycle['ADJUSTMENTS'].groupby(item_cycle['INV_DATE']).agg(np.sum)
    
    cycle_stats = basic_stats(day_cycle)
    
    # Converts datetimes to calculate last cycle count.
    day_cycle.index = pd.to_datetime(day_cycle.index)
    recent_date = day_cycle.index.max()
    recent_date = recent_date.date()
    time_since = dt.date.today() - recent_date
    
    # Dictionary with all relelevant cycle info.
    cycle_data = {'cycle_mean':cycle_stats['mean'], 'cycle_std':cycle_stats['std'],
                  'recent_date':recent_date, 'time_since': time_since}
    return cycle_data
    

def faux_report(sales_data, cycle_data):   
    print 'Item Number:{0}, aka: {1}.'.format(sales_data['item_num'],sales_data['item_desc'])
    print 'The item has a purchase mean of {0} and a standard deviation of {1}.'.format(sales_data['sales_mean'],sales_data['sales_std'])
    print 'Per day mean of {0} and standard deviation of {1}.'.format(sales_data['day_mean'],sales_data['day_std'])
    print 'The top 5 customers, with percentage of sales are:', sales_data['top_5']
    print 'The average variance on a cycle count is {0} with a standard devation of {1}'.format(cycle_data['cycle_mean'],cycle_data['cycle_std'])
    print 'The last cycle count occured {0}, roughly {1} days ago.' .format(cycle_data['recent_date'], cycle_data['time_since'])
    
item_number = raw_input ('What is the item number you are looking for? ')

s_data = sales_info(item_number)
c_data = cycle_info(item_number)

print faux_report(s_data, c_data)
    

'''
by day
  std
  mean
by sale
  std
  mean

hist by sale
hist by day

plot by day
plot by months

'''
