# -*- coding: utf-8 -*-

import pandas as pd
import pandas_datareader.data as web   # Package and modules for importing data; this code may change depending on pandas version
import datetime
import numpy as np
import os
import random
from datetime import timedelta
import statsmodels.api as sm
# SARIMAX example
from statsmodels.tsa.statespace.sarimax import SARIMAX
import sys, getopt
# We will look at stock prices over the past year, starting at January 1, 2016



def getStartDate(end,months):
    day=end.day
    year=end.year-months//12-1
    month=months%12+1
    start=datetime.datetime(year,month,day)
    return start

def loadStocksByTickers(scraped_tickers,path,outputfile,months=12):
    end = datetime.date.today()
    savepath=path+outputfile
    errorpath=path+'errors.csv'
    #end =datetime.datetime(end.year,end.month,1).date()
    
    ds =pd.DataFrame()
    exist_ds=pd.DataFrame()
    errors=pd.DataFrame([],columns=['item'])
    errorexists=os.path.isfile(errorpath)
    print('exists error',errorexists)
    if(errorexists):
        errors=pd.read_csv(errorpath,index_col=0)
    exists = os.path.isfile(savepath)
    print(savepath,'exists file',exists)
    if exists:
        exist_ds=pd.read_csv(savepath,parse_dates=['Date'],index_col='Date')
    
    for item in scraped_tickers:
        try:
            if  len(errors)>0 and errors['item'].str.contains(item).any():
                print(item,'occured an exception before. skip this time.')
            else:
                if(exists and exist_ds.columns.contains(item)):
                    start=exist_ds[item].index[-1].date()
                    print(item,' exists and update between',start,end,start<end)
                    res=None
                    new_end=end-timedelta(days=1)
                    if(start<new_end):
                        remains=web.DataReader(item,"yahoo",start,new_end)['Adj Close']              
                        res=exist_ds[item].combine_first(remains)
                    else:
                        res=exist_ds[item]
    
                    exist_ds[item] =res
                    ds[item]=res
                else:
                    start=getStartDate(end,months).date()
                    print(item,'is new and load from yahoo between',start,end,start<end)
                    res=web.DataReader(item,"yahoo",start,end)['Adj Close']
                    ds[item]=res
                    exist_ds[item] =res
        
        except Exception as e: 
    
            da=pd.DataFrame([item],columns=errors.columns)
            print(item,'write in errors.csv',e)
            if(not str(e).find('No data fetched for symbol')==-1):
                errors=errors.append(da,ignore_index=True)
            pass
    if(exist_ds.isna().all().sum()>0):
        exist_ds[exist_ds.columns[exist_ds.isna().all()]].dropna(axis=1,inplace=True)
    exist_ds.columns[exist_ds.isna().any()].any()
    #savepath='/Users/pengwang/Dropbox/finance/ttest.csv'
    errors.to_csv(errorpath)
    exist_ds.to_csv(savepath)
    return ds


def loadAuInfoTickersFromYahooExcel(inputFile):

    stock_names=pd.read_excel(inputFile,header=3,usecols=4)
    
    au_stocks=stock_names[stock_names['Country']=='Australia']
    au_tickers=au_stocks[au_stocks['Category Name']=='Apparel Stores']['Ticker']
    scraped_tickers =au_tickers.tolist()
    return scraped_tickers
def loadAuNotNaTickersFromYahooExcel(inputFile):

    stock_names=pd.read_excel(inputFile,header=3,usecols=4)
    
    au_stocks=stock_names[stock_names['Country']=='Australia']
    au_tickers=au_stocks[au_stocks['Ticker'].notna()]['Ticker']
    scraped_tickers =au_tickers.tolist()
    return scraped_tickers
def loadUSANotNaTickersFromYahooExcel(inputFile):

    stock_names=pd.read_excel(inputFile,header=3,usecols=4)
    
    au_stocks=stock_names[stock_names['Country']=='USA']
    au_tickers=au_stocks[au_stocks['Ticker'].notna()]['Ticker']
    scraped_tickers =au_tickers.tolist()
    return scraped_tickers

path='/root/pythondev/JanePython/'
inputfile = path+'ASXListedCompanies.csv'
outputfile = 'stocks2.csv'

da=pd.read_csv(inputfile,header=1)
ticker=da.iloc[:,1].tolist()
stocks=loadStocksByTickers(tickers,path,outputfile)
stocks=loadStocksByTickers(tickers,path,outputfile)
