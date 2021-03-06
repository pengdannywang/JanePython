from datetime import datetime
import time
import pandas as pd
import warnings

from sarimaxModel import selectParameters
from sarimaxModel import sarimaxPrdict
import multiprocessing
import psutil
warnings.filterwarnings('ignore')
data=pd.read_csv('/Users/pengwang/work/stocks.csv',parse_dates=['Date'],index_col='Date')
data=data.resample('MS').mean()


def evaluateStock(item,steps=6):
    
    y=data[item]


    p1,p2,t,err=selectParameters(y,steps=3,disp=False)

    pred=sarimaxPrdict(y,p1,p2,t,steps=3,disp=False)

    return pred
start=datetime.now()
pool=multiprocessing.Pool(processes=15)
result=pd.DataFrame()
    
scraped_tickers = ['GWW', 'ABT','SRE','PCAR', 'ITW', 'ILMN']

for item in scraped_tickers:
    
    result[item]=pool.apply(evaluateStock,(item,))
procs = list() 

pool.close()
pool.join
end=datetime.now()
period=end-start
print("total period==",period.seconds)
print(result.head())