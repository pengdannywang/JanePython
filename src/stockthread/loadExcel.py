# -*- coding: utf-8 -*-
import sys, getopt
import pandas as pd
from sarimaxModel import forcastStocks
from loadstocks import loadStocksByTickers
from loadstocks import loadAuTickersFromYahooExcel
# We will look at stock prices over the past year, starting at January 1, 2016

path='/Users/pengwang/Dropbox/finance/'
inputfile = path+'Yahoo.xlsx'
outputfile = path+'stocks.csv'
rlow=0
rmax=500

    

result=data[-1:].append(result)
result.to_csv(path+'predicts.csv')
x=result.diff()
invest=1000
cost=10
benefit=(x*invest)/result-10


def main(argv):
    global path
    global inputfile
    global outputfile 
    global rlow
    global rmax
    try:
        opts, args = getopt.getopt(argv,"hi:o:p:l:m:",["ifile=","ofile=","path=","low=","max="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('loadstocks.py -p <path> -i <inputfile> -o <outputfile>',"-l number","-m number")
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-l", "--low"):
            rlow = arg
        elif opt in ("-m", "--max"):
            rmax = arg
    inputfile=path+inputfile

    
    executeProgram(inputfile,outputfile,r_low=rlow,r_max=rmax)
        
def executeProgram(inputfile,outputfile,r_low=0,r_max=500):

    tickers=loadAuTickersFromYahooExcel(inputfile)
    tickers=tickers[r_low:r_max]
    stocks=loadStocksByTickers(tickers,path,outputfile)

    data=stocks.resample('MS').mean()
    result=pd.DataFrame()
    for ticker in data.columns:
        result[ticker]=forcastStocks(path+'parameters.csv',ticker,data[ticker])

if __name__ == "__main__":
   main(sys.argv[1:])