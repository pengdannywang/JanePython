
import time
import pandas as pd
import warnings
from optParameterThreads import optimizeParameter
from sarimaxModel import sarimaxPrdict
import multiprocessing
warnings.filterwarnings('ignore')
data=pd.read_csv('/Users/pengwang/work/stocks.csv',parse_dates=['Date'],index_col='Date')
data=data.resample('MS').mean()


def evaluateStock(item,steps=6):
    
    y=data[item]


    p1,p2,t,err=optimizeParameter(y,steps=6,disp=False)

    pred=sarimaxPrdict(y,p1,p2,t,steps=3,disp=False)

    return pred

pool=multiprocessing.Pool(processes=60)
result=pd.DataFrame()
    

for item in data.columns:
    
    result[item]=pool.apply(evaluateStock,(item,))
    
pool.close()
pool.join
print(result.head())