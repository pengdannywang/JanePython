import pandas as pd
import warnings
from datetime import datetime
from sarimaxModel import selectParameters
from sarimaxModel import sarimaxPrdict
warnings.filterwarnings('ignore')
data=pd.read_csv('/Users/pengwang/work/stocks.csv',parse_dates=['Date'],index_col='Date')

y=data.resample('MS').mean()
 
        
def evaluateStock(item,steps=3):

 
    p1,p2,t,err=selectParameters(y,steps=6,disp=False)
    pred=sarimaxPrdict(y,p1,p2,t,steps=3,disp=False)
    return pred
start=datetime.now()
scraped_tickers = ['CHK', 'UA','UAA','NTAP', 'DLPH']
id=1
result=pd.DataFrame()
for item in scraped_tickers:
    thread=myThread(id,item)
    thread.start()
    threads.append(thread)
    id+=1
    
for t in threads:
    t.join()
    result[t.get_item()]=t.get_value()
end=datetime.now()
period=end-start
print("total period==",period.seconds)
print(result)