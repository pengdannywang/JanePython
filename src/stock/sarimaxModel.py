import pandas as pd
import pandas_datareader.data as web   # Package and modules for importing data; this code may change depending on pandas version
import datetime
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
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.stattools import adfuller
data=pd.read_csv('u:/python/test/stocks.csv',parse_dates=['Date'],index_col='Date')

import matplotlib.pylab as plt
import itertools
    


res=data.resample('MS').mean()
y=res['GOOGL']
train_y,test_y=y[:-6],y[-6:]
def selectParameters(train_y,test_y):
    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 2)
    
    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))
    
    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [[x[0], x[1], x[2], 12] for x in list(itertools.product(p, d, q))]
    # fit model

    mses=pd.DataFrame()
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                model = sm.tsa.statespace.SARIMAX(train_y,
                                     order=param,
                                     seasonal_order=param_seasonal,
                                     enforce_stationarity=False,
                                     enforce_invertibility=False)
     
                steps=len(test_y)
                model_fit = model.fit()
                #print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, model_fit.aic))
                pred=model_fit.forecast(steps=steps)
    #            print(pred)
    #            print(test_y)
                #print('mse:{}'.format(mean_squared_error(test_y,pred)))
                
                mses=mses.append([list(param)+list(param_seasonal)+[mean_squared_error(test_y,pred),model_fit.aic]],ignore_index=True)
                
            except :
                #print('ARIMA{} error:{}'.format(param,e))
                pass
    #model_fit=model.fit(disp=0)
    mses=mses.sort_values(mses.columns[-1])
    para=mses[0:1].values
    return para
para=selectParameters(train_y,test_y)
print("para:{}".format(para))
param=list(para[0,0:3].astype(int))
ps=list(para[0,3:7].astype(int))
print(param)
print(ps)
model = sm.tsa.statespace.SARIMAX(train_y,
                                     order=param,
                                     seasonal_order=[0,1,0,12],
                                     enforce_stationarity=False,
                                     enforce_invertibility=False)

model_fit = model.fit()

pred=model_fit.get_prediction(start='2018-10-01',end='2019-03-01', dynamic=True)
pred_ci = pred.conf_int()
ax = y['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Date')
ax.set_ylabel('CO2 Levels')
plt.legend()

plt.show()
       