%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
Rtl_data=pd.read_csv('Retail.csv',encoding='unicode_escape')
# Rtl_data.head()
country_cast_data=Rtl_data[['Country','CustomerID']].drop_duplicates()
country_cast_data.groupby(['Country'])['CustomerID'].aggregate('count').reset_index().sort_values('CustomerID',ascending=False)
Rtl_data=Rtl_data.query("Country=='United Kingdom'").reset_index(drop=True)
Rtl_data.isnull().sum(axis=0)
Rtl_data= Rtl_data[pd.notnull(Rtl_data['CustomerID'])]
Rtl_data.Quantity.min()
Rtl_data.UnitPrice.min()
Rtl_data=Rtl_data[(Rtl_data['Quantity']>0)]
Rtl_data['InvoiceDate']=pd.to_datetime(Rtl_data['InvoiceDate'])
Rtl_data['TotalAmount']=Rtl_data['Quantity']*Rtl_data['UnitPrice']
#Rtl_data.head()
import datetime as dt
Latest_Date= dt.datetime(2011,12,10)
RFMScores = Rtl_data.groupby('CustomerID').agg({'InvoiceDate': lambda x: (Latest_Date - x.max()).days, 'InvoiceNo': lambda x: len(x), 'TotalAmount': lambda x: x.sum()})
# RFMScores['InvoiceDate'] = RFMScores['InvoiceDate'].astype(int)
RFMScores['InvoiceDate']=pd.to_numeric(RFMScores['InvoiceDate'])

RFMScores.rename(columns={'InvoiceDate': 'Recency', 'InvoiceNo': 'Frequency', 'TotalAmount': 'Monetary'}, inplace=True)
RFMScores.reset_index().head()
quantiles = RFMScores.quantile(q=[0.25,0.5,0.75])
quantiles = quantiles.to_dict()
quantiles
def RScoring(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4
    
def FnMScoring(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1
RFMScores['R'] = RFMScores['Recency'].apply(RScoring, args=('Recency',quantiles,))
RFMScores['F'] = RFMScores['Frequency'].apply(FnMScoring, args=('Frequency',quantiles,))
RFMScores['RFMGroup'] = RFMScores.R.map(str) + RFMScores.F.map(str) + RFMScores.M.map(str)
RFMScores['RFMScore'] = RFMScores[['R', 'F', 'M']].sum(axis = 1)
Loyalty_Level = ['Platinum', 'Gold', 'Silver', 'Bronze']
Score_cuts = pd.qcut(RFMScores.RFMScore, q = 4, labels = Loyalty_Level)
RFMScores['RFM_Loyalty_Level'] = Score_cuts.values
RFMScores.reset_index().head()
RFMScores['M'] = RFMScores['Monetary'].apply(FnMScoring, args=('Monetary',quantiles,))
RFMScores.head()