# -*- coding: utf-8 -*-

import pandas as pd
from sarimaxModel import forcastStocks
from loadstocks import loadStocksByTickers
from loadstocks import loadAuTickersFromYahooExcel
# We will look at stock prices over the past year, starting at January 1, 2016

path='/Users/pengwang/Dropbox/finance/'
inputfile = path+'Yahoo.xlsx'
outputfile = path+'stocks.csv'
tickers=['BMP.AX','REA.AX','CPU.AX']
tickers=loadAuTickersFromYahooExcel(inputfile)
stocks=loadStocksByTickers(tickers,outputfile)
data=stocks.resample('MS').mean()
result=pd.DataFrame()
param=pd.DataFrame()
for ticker in data.columns:
    pred=forcastStocks(path+'parameters.csv',ticker,data[ticker])
    result[ticker]=pred
    

result=data[-1:].append(result)
result.to_csv(path+'predicts.csv')
x=result.diff()
invest=1000
cost=10
benefit=(x*invest)/result-10