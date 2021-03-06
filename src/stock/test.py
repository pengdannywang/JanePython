import pandas as pd

from datetime import datetime
import os
import numpy as np
import random
import statsmodels.api as sm
from matplotlib import pyplot
# SARIMAX example
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARIMA
from random import random
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.stattools import adfuller

import queue
import threading
import time
import matplotlib.pylab as plt
import itertools
import math
import warnings

warnings.filterwarnings('ignore')

def measure_rmse(actual, predicted):
	return math.sqrt(mean_squared_error(actual, predicted))

def selectParameters(y,test_y,disp=False):
    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 2)

    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))

    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [[x[0], x[1], x[2], 12] for x in list(itertools.product(p, d, q))]
    # fit model
    trend_c=['n','c','t','ct']
    mses=pd.DataFrame()
    error=pd.DataFrame()
    parameters=[]
    forcast=None
    for param in pdq:
        for t in trend_c:
            for param_seasonal in seasonal_pdq:
                try:
                    model = sm.tsa.statespace.SARIMAX(y,
                                         order=param,
                                         seasonal_order=param_seasonal,
                                         trend=t,
                                         enforce_stationarity=False,
                                         enforce_invertibility=False)

                    model_fit = model.fit(disp=False)

                    pred=model_fit.forecast(steps=len(test_y))
        #            print(pred)
        #            print(test_y)
                    #print('mse:{}'.format(mean_squared_error(test_y,pred)))
                    mse=measure_rmse(test_y,pred)
                    mses=mses.append([list(param)+list(param_seasonal)+[t]+[model_fit.aic]+[mse]],ignore_index=True)

                    if parameters==[] or parameters[-1]>mse:
                        parameters=list(param)+list(param_seasonal)+[t]+[model_fit.aic]+[mse]
                        forcast=pred
                    
                except :

                    #print('ARIMA{} error:{}'.format(param,e))
                    error=error.append([list(param)+list(param_seasonal)+[t]],ignore_index=True)

                    pass
    #model_fit=model.fit(disp=0)
    if disp:

        print(parameters)
        pred_ci=pd.DataFrame(index=forcast.index)
        pred_ci['low'] = forcast-forcast*0.05
        pred_ci['upper'] = forcast+forcast*0.05


        #pred_ci.loc[y.index[-1]]=[y[-1],y[-1]]
        #pred_ci=pred_ci.sort_index()
        ax = y['2018':].plot(label='observed')
        forcast.plot(ax=ax, label='Forecast', alpha=.7)
        
        ax.fill_between(forcast.index,
                        pred_ci.iloc[:,0],
                        pred_ci.iloc[:,1], color='k', alpha=.1)
        
        ax.set_xlabel('Date')
        ax.set_ylabel(y.name)
        plt.legend()
        
        plt.show()
    p1,p2,t,err=parameters[0:3],parameters[3:7],parameters[7],parameters[-1]

    return p1,p2,t,err


def sarimaxPrdict(train_y, p_order, p_seasonal_order, vtrend, steps=1, disp=False):

    model = sm.tsa.statespace.SARIMAX(train_y,
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
    def __init__(self,threadId,param,param_seasonal,trend,train_y,test_y):
        threading.Thread.__init__(self)
        self.train_y=train_y
        self.test_y=test_y
        self.param=param
        self.param_seasonal=param_seasonal
        self.trend=trend
        self.mse=-1
        self.threadId=threadId
        
    def run(self):
        print('thread: {}',self.threadId)
        self.mse=sarimaxTest(self.param,self.param_seasonal,self.trend,self.train_y,self.test_y)
            
        
    def get_mse(self):
        return self.mse

    def get_param(self):
        return self.param,self.param_seasonal,self.trend
    
    
def sarimaxTest(param,param_seasonal,trend,train_y,test_y,disp=True):
    mse=-1
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
        
    except :
        mse=-1

    return mse
data=pd.read_csv('/Users/pengwang/work/stocks.csv',parse_dates=['Date'],index_col='Date')
data=data.resample('MS').mean()
y=data['ABT']
steps=3
disp=True
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
threadId=1
for param in pdq:
    for t in trend_c:
        for param_seasonal in seasonal_pdq:
            
            thread=myThread(threadId,param,param_seasonal,t,train_y,test_y)
            thread.start()
            threads.append(thread)
            threadId+=1

for thread in threads :
    thread.join()
    mse=thread.get_mse()
    if(mse>0  ):
        param,param_seasonal,t=thread.get_param()
        mses=mses.append([list(param)+list(param_seasonal)+[t]+[mse]],ignore_index=True)

parameter=[]
if len(mses)>0:     
    mses=mses.sort_values(mses.columns[-1])
    parameter=mses[0:1].values

# model_fit=model.fit(disp=0)
if disp:
    print(parameter)
    param,param_seasonal,trend=parameter[0:3],parameter[3:7],parameter[7]
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


