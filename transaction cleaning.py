# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 19:06:04 2016

@author: Gerard
"""

import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

#initial part cleans out whitespace and the trailing negative
'''
clean_tran = open('INVENTORY_TRANSACTIONS_COMPLETE.csv','rb')
new_file = open('INVENTORY_CLEANED_AGAIN.csv','wb')

with clean_tran as csvfile:
    cleaning = csv.reader(csvfile, delimiter = ',')
    cleaned = csv.writer(new_file)
    for row in cleaning:
        temp_row = []
        for cell in row:
            cell = cell.strip()
            temp_row.append(cell)
        if '-' in temp_row[8]:
            temp_row[8] = temp_row[8].replace('-','')
            temp_row[8] = '-'+ temp_row[8]
        if '-' in temp_row[10]:
            temp_row[10] = temp_row[10].replace('-','')
            temp_row[10] = '-'+ temp_row[10]    
        #temp_row[9] = temp_row[9].replace('-','')
        cleaned.writerow(temp_row)
new_file.close()
'''

# Further cleaning of the tables that will be used.         
inv_tran = pd.read_csv('INVENTORY_CLEANED_AGAIN.csv')
inv_tran['INV_DATE']= pd.to_datetime(inv_tran['INV_DATE'], format = '%m/%d/%Y')

sales_tran = inv_tran[np.isfinite(inv_tran['SALES'])]
sales_tran = sales_tran.drop(['ADJUSTMENTS', 'RECEIPTS', 'RETURNS'],1)
sales_tran['SALES'] = sales_tran['SALES'].apply(lambda x:x*-1)

po_tran = inv_tran[np.isfinite(inv_tran['RECEIPTS'])]
po_tran = po_tran.drop(['ADJUSTMENTS', 'SALES', 'RETURNS'],1)

cycle_tran = inv_tran[np.isfinite(inv_tran['ADJUSTMENTS'])]
cycle_tran = cycle_tran.drop(['RECEIPTS', 'SALES', 'RETURNS'],1)

# should remove inventory and replace too
adj_tran = cycle_tran[cycle_tran['TRAN_DOC'] != 'CYCLE']

cycle_tran = cycle_tran[cycle_tran['TRAN_DOC'] == 'CYCLE']
cycle_tran = cycle_tran.drop(['CUST_NUM', 'CUST_NAME'],1)

ret_tran = inv_tran[np.isfinite(inv_tran['RETURNS'])]
ret_tran = ret_tran.drop(['RECEIPTS', 'SALES', 'ADJUSTMENTS'],1)

inv_tran.to_csv('inv_tran.csv' ,index =False)
sales_tran.to_csv('sales_tran.csv', index=  False)
po_tran.to_csv('po_tran.csv' ,index=  False)
cycle_tran.to_csv('cycle_tran.csv', index= False)
ret_tran.to_csv('ret_tran.csv' ,index = False)
adj_tran.to_csv('adj_tran.csv',index = False) 

'''
charcoal = inv_tran[inv_tran['ITEM_NUM'] == '02GASTP3CH']

charcoal = charcoal[['ITEM_NUM','SALES', 'INV_DATE']]
charcoal = charcoal.dropna(0,'any')
charcoal['INV_DATE'] = pd.to_datetime(charcoal['INV_DATE'], format = '%m/%d/%Y')



print charcoal['SALES'].mean()
print charcoal['SALES'].std()

day_group = charcoal['SALES'].groupby(charcoal['INV_DATE'])
by_day = day_group.agg(np.sum)



plt.figure()
by_day.hist(bins = 50)
print by_day.mean()
print by_day.std()

#charcoal.to_csv('Charcoal_Sales.csv')

'''