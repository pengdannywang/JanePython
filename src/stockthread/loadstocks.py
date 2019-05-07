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

def loadStocksByTickers(scraped_tickers,path,outputfile,months=18):
    end = datetime.date.today()
    savepath=path+outputfile
    errorpath=path+'errors.csv'
    #end =datetime.datetime(end.year,end.month,1).date()
    file=pd.DataFrame()
    ds =pd.DataFrame()
    errors=pd.DataFrame([],columns=['item'])
    errorexists=os.path.isfile(errorpath)
    print('exists error',errorexists)
    if(errorexists):
        errors=pd.read_csv(errorpath,index_col=0)
    exists = os.path.isfile(savepath)
    print(savepath,'exists file',exists)
    if exists:
        ds=pd.read_csv(savepath,parse_dates=['Date'],index_col='Date')
    
    for item in scraped_tickers:
        try:
            print(len(errors)==0 , errors['item'].str.contains(item).any())
            if  len(errors)>0 and errors['item'].str.contains(item).any():
                print(item,'exists in errors.csv')
            else:
                if(exists and ds.columns.contains(item)):
                    start=ds[item].index[-1].date()
                    print(item,' exist date::',start,end,start<end)
                    res=None
    
                    if(start<end):
                        remains=web.DataReader(item,"yahoo",start,end)['Adj Close']              
                        res=file[item].combine_first(remains)
                    else:
                        res=file[item]
    
                    ds[item] =res
                else:
                    start=getStartDate(end,months).date()
                    print(item,'new date2::',start,end,start<end)
                    res=web.DataReader(item,"yahoo",start,end)['Adj Close']
                    ds[item]=res
        
        except Exception as e: 
    
            da=pd.DataFrame([item],columns=errors.columns)
            if(not str(e).find('No data fetched for symbol')==-1):
                print(item,'write in errors.csv',e)
                errors=errors.append(da,ignore_index=True)
            pass
    if(ds.isna().all().sum()>0):
        ds[ds.columns[ds.isna().all()]].dropna(axis=1,inplace=True)
    ds.columns[ds.isna().any()].any()
    #savepath='/Users/pengwang/Dropbox/finance/ttest.csv'
    errors.to_csv(errorpath)
    ds.to_csv(savepath)
    return ds

def loadAuTickersFromYahooExcel(inputFile):

    stock_names=pd.read_excel(inputFile,header=3,usecols=4)
    
    au_stocks=stock_names[stock_names['Country']=='Australia']
    au_tickers=au_stocks[au_stocks['Category Name'].str.contains('Information',regex=True,na=False)]['Ticker']
    scraped_tickers =au_tickers.tolist()
    return scraped_tickers

def main(argv):
    path='U:/python/JanePython/'
    inputfile = 'Yahoo.xlsx'
    outputfile = 'predicts.csv'
    try:
        opts, args = getopt.getopt(argv,"hi:o:p:",["ifile=","ofile=","path="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('loadstocks.py -p <path> -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    inputfile=path+inputfile
    outputfile=path+outputfile
    return inputfile,outputfile




   