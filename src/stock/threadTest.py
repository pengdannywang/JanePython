import pandas as pd
import warnings
from datetime import datetime
from optParameterThreads import optimizeParameter
from sarimaxModel import sarimaxPrdict
warnings.filterwarnings('ignore')
data=pd.read_csv('/Users/pengwang/work/stocks.csv',parse_dates=['Date'],index_col='Date')
name='HES'
y=data[name].resample('MS').mean()
      
import queue
import threading
import time

exitFlag = 0
threads=[]
class myThread (threading.Thread):
    def __init__(self, threadID, item):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.item = item
        self.pred=None
    def run(self):
        start=datetime.now()
        print("thread:",self.threadID,self.item ,",start=",start)
        self.pred=evaluateStock(self.item)
        end=datetime.now()-start
        print("thread period=",self.threadID,self.item ,end.seconds)
        
    def get_value(self):
        return self.pred
    
    def get_item(self):
        return self.item
        
def evaluateStock(item,steps=3):

 
    p1,p2,t,err=optimizeParameter(y,steps=6,disp=False)
    pred=sarimaxPrdict(y,p1,p2,t,steps=3,disp=False)
    return pred
start=datetime.now()
scraped_tickers = ['MMM', 'ABT', 'ABBV', 'ITW', 'ILMN']
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

