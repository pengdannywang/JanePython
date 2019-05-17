# -*- coding: utf-8 -*-

import pandas as pd
from sarimaxModel import forcastStocks
from loadstocks import loadStocksByTickers
from loadstocks import loadAuTickersFromYahooExcel
# We will look at stock prices over the past year, starting at January 1, 2016

path='/Users/pengwang/Dropbox/finance/'
inputfile = path+'Yahoo.xlsx'
outputfile = path+'stocks.csv'

tickers=loadAuTickersFromYahooExcel(inputfile)
print(tickers)

tickers=['BMP.AX', 'REA.AX', 'CPU.AX', 'TCN.AX', 'DWS.AX', 'TME.AX', 'EPD.AX', 'RAP.AX', 'GLH.AX', 'GBT.AX', 'SMX.AX', 'MLB.AX', 'NWZ.AX', 'ADJ.AX', 'ALC.AX', 'ICQ.AX', 'SEK.AX', 'COO.AX', 'CGO.AX', 'PME.AX', 'MUA.AX', 'ECG.AX', 'DTL.AX', 'CNW.AX', 'CGS.AX', 'CAR.AX', '1ST.AX', 'ONE.AX', 'OHE.AX', 'JHL.AX', 'ICS.AX', 'ISU.AX', 'IVO.AX', 'LAA.AX', 'MDR.AX', 'NEA.AX', 'PSZ.AX', 'RNT.AX']
#tickers=loadAuTickersFromYahooExcel(inputfile)
stocks=loadStocksByTickers(tickers,outputfile)
print(stocks)