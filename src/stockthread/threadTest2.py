import pandas as pd
import warnings
from datetime import datetime
from sarimaxModel import selectParameters
from sarimaxModel import sarimaxPrdict
warnings.filterwarnings('ignore')
data=pd.read_csv('u:/python/test/stocks.csv',parse_dates=['Date'],index_col='Date')
data=data['2018-01-01':]
y=data.resample('MS').mean()

      
import queue
import threading
import time

exitFlag = 0
threads=[]
class myThread (threading.Thread):
    def __init__(self, threadID, item,data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.item = item
        self.data=data
        self.pred=None
    def run(self):
        start=datetime.now()
        
        self.pred=evaluateStock(self.data[self.item])
        end=datetime.now()-start
        
        
    def get_value(self):
        return self.pred
    
    def get_item(self):
        return self.item
        
def evaluateStock(y,steps=3):

    p1,p2,t,err=selectParameters(y,steps=3,disp=False)
    pred=sarimaxPrdict(y,p1,p2,t,steps=3,disp=False)
    return pred

start=datetime.now()
scraped_tickers = ['MMM', 'ABT', 'ABBV', 'ACN', 'ATVI', 'AYI', 'ADBE', 'AMD', 'AAP',   'AMG', 'AFL', 'A']
id=1
result=pd.DataFrame()
for item in scraped_tickers:
    thread=myThread(id,item,y)
    thread.start()
    threads.append(thread)
    id+=1
    
for t in threads:
    t.join()
    result[t.get_item()]=t.get_value()
end=datetime.now()
period=end-start
print('period:::',period.seconds)
result=y[scraped_tickers][-1:].append(result)
result.to_csv('u:/python/test/predicts.csv')
x=result.diff()
invest=1000
cost=10
benefit=(x*invest)/result-10
