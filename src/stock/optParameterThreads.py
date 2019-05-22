
import pandas as pd

import pandas_datareader.data as web 
import statsmodels.api as sm
import os
# SARIMAX example
from statsmodels.tsa.statespace.sarimax import SARIMAX

from sklearn.metrics import mean_squared_error


import matplotlib.pylab as plt
import itertools
import math
import warnings
import datetime
from datetime import timedelta
import queue
import threading

warnings.filterwarnings('ignore')

def measure_rmse(actual, predicted):
	return math.sqrt(mean_squared_error(actual, predicted))



def sarimaxPrdict(train_y, p_order, p_seasonal_order, vtrend, steps=1, disp=False):

    model = SARIMAX(train_y,
          order=p_order,
          seasonal_order=p_seasonal_order,
          trend=vtrend,
          enforce_stationarity=False,
          enforce_invertibility=False)

    model_fit = model.fit(disp=False)

    pred=model_fit.forecast(steps=steps)
    if disp:
        pred_ci=pd.DataFrame(index=pred.index)
        pred_ci['low'] = pred-pred*0.05
        pred_ci['upper'] = pred+pred*0.05
        
        
        #pred_ci.loc[y.index[-1]]=[y[-1],y[-1]]
        #pred_ci=pred_ci.sort_index()
        ax = train_y['2018':].plot(label='observed')
        pred.plot(ax=ax, label='Forecast', alpha=.7)
        
        ax.fill_between(pred.index,
                        pred_ci.iloc[:,0],
                        pred_ci.iloc[:,1], color='k', alpha=.1)
        
        ax.set_xlabel('Date')
        ax.set_ylabel(train_y.name)
        plt.legend()
        
        plt.show()
    return pred





class myThread (threading.Thread):
    def __init__(self,ticker,param,param_seasonal,trend,train_y,test_y):
        threading.Thread.__init__(self)
        self.train_y=train_y
        self.test_y=test_y
        self.param=param
        self.param_seasonal=param_seasonal
        self.trend=trend
        self.mse=1000
        self.ticker=ticker
        self.aic=-1
    def run(self):
        try:
            self.aic,self.mse=sarimaxTest(self.param,self.param_seasonal,self.trend,self.train_y,self.test_y)
        except:
            print('except',self.aic)
            self.aic,self.mse=-1,1000
            pass
            
        
    def get_mse(self):
        return self.mse

    def get_param(self):
        return [[self.ticker]+list(self.param)+list(self.param_seasonal)+[self.trend,self.aic,self.mse]]
    
    
def sarimaxTest(param,param_seasonal,trend,train_y,test_y):
    mse=1000

    try:
        model = sm.tsa.statespace.SARIMAX(train_y,
                             order=param,
                             seasonal_order=param_seasonal,
                             trend=trend,
                             enforce_stationarity=False,
                             enforce_invertibility=False)

        model_fit = model.fit(disp=False)

        pred=model_fit.forecast(steps=len(test_y))
#            print(pred)
#            print(test_y)
        #print('mse:{}'.format(mean_squared_error(test_y,pred)))
        mse=measure_rmse(test_y,pred)
        return model_fit.aic,mse
    except :
        pass
        
    return -1,1000
    

def optimizeParameter(ticker,y, steps=1,disp=False):
    train_y, test_y = y[:-steps], y[-steps:]
      # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 2)

    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))

    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [[x[0], x[1], x[2], 12] for x in list(itertools.product(p, d, q))]
    # fit model
    trend_c=['n','c','t','ct']
    mses=pd.DataFrame()
    threads=[]
    q = queue.Queue()

    for param in pdq:
        for t in trend_c:
            for param_seasonal in seasonal_pdq:
                
                thread=myThread(ticker,param,param_seasonal,t,train_y,test_y)
                thread.start()
                threads.append(thread)
    

    for thread in threads :
        thread.join()
        mse=thread.get_mse()
        if(mse>0  ):
            param=thread.get_param()
            mses=mses.append(param,ignore_index=True)

    parameter=[]
    if len(mses)>0:     
        mses=mses.sort_values(mses.columns[-1])
        parameter=mses[0:1].values[0]

    # model_fit=model.fit(disp=0)
    if disp:
        print(parameter)
        param,param_seasonal,trend=parameter[1:4],parameter[4:8],parameter[8]
        model = sm.tsa.statespace.SARIMAX(train_y,
                                          order=param,
                                          seasonal_order=param_seasonal,
                                          trend=trend,
                                          enforce_stationarity=False,
                                          enforce_invertibility=False)

        model_fit = model.fit(disp=False)

        forcast = model_fit.forecast(steps=len(test_y))
        pred_ci = pd.DataFrame(index=forcast.index)
        pred_ci['low'] = forcast - forcast * 0.05
        pred_ci['upper'] = forcast + forcast * 0.05

        # pred_ci.loc[y.index[-1]]=[y[-1],y[-1]]
        # pred_ci=pred_ci.sort_index()
        ax = y['2018':].plot(label='observed')
        forcast.plot(ax=ax, label='Forecast', alpha=.7)

        ax.fill_between(forcast.index,
                        pred_ci.iloc[:, 0],
                        pred_ci.iloc[:, 1], color='k', alpha=.1)

        ax.set_xlabel('Date')
        ax.set_ylabel(y.name)
        plt.legend()

        plt.show()

    return parameter

def dynamicForacast(ticker,y,steps=1,disp=False):
    paramPath='/root/pythondev/JanePython/parameters1.csv'
    p1,p2,t=[],[],''
    result=None
    exists = os.path.isfile(paramPath)
    params=pd.DataFrame([],columns=['p1','p2','p3','p4','p5','p6','p7','trend','aic','mse'])
    if(exists):
        params=pd.read_csv(paramPath,index_col=0)
    parameters=optimizeParameter(ticker,y,steps=steps,disp=False)
    print('new calculated parameter:',parameters)
    if(len(parameters)>8):
        p1,p2,t=parameters[1:4],parameters[4:8],parameters[8]
 
    try: 
        if not (p1==[] or p2==[] or t==''):
            result=sarimaxPrdict(y,p1,p2,t,steps=3,disp=disp)
            params.loc[ticker]=parameters[1:]
            params.to_csv(paramPath) 
    except Exception as e: 
        print('unable to do prediction,parameter:',ticker, ' errors::',e)
        
    return result

path='/root/pythondev/JanePython/'
inputfile = path+'Yahoo.xlsx'
outputfile = 'stocks2.csv'
savepath=path+outputfile
data=pd.read_csv(savepath,parse_dates=['Date'],index_col='Date')
data=data[[col for col in data.columns if pd.Series(data[col].values>1).sum()>30]]
data=data.resample('W').mean()

result=pd.DataFrame()
for ticker in data.columns:
    print(ticker)
    res=dynamicForacast(ticker,data[ticker])
    if(res is not None):
        result[ticker]=res

result.to_csv(path+'/weeklyforecast.csv')