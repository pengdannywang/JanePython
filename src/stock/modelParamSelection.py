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
y=res['LOW']
train_y,test_y=y[:-3],y[-3:]
# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
# fit model
model=ARIMA(train_y,order=(1,1,0))
mses=pd.DataFrame()
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            model = sm.tsa.statespace.SARIMAX(train_y,
                                 order=param,
                                 seasonal_order=param_seasonal,
                                 enforce_stationarity=False,
                                 enforce_invertibility=False)
 

            model_fit = model.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, model_fit.aic))
            pred=model_fit.predict(start='2019-01',end='2019-03')
#            print(pred)
#            print(test_y)
            #print('mse:{}'.format(mean_squared_error(test_y,pred)))
            
            mses=mses.append([list(param)+list(param_seasonal)+[mean_squared_error(test_y,pred)]],ignore_index=True)
            
        except Exception as e:
            print('ARIMA{} error:{}'.format(param,e))
            continue
#model_fit=model.fit(disp=0)
mses=mses.sort_values(mses.columns[-1])
para=mses[0:1].values[0]
print(para)
model = sm.tsa.statespace.SARIMAX(train_y,
                                 order=para[0:3].astype(int),
                                 seasonal_order=para[3:7].astype(int),
                                 enforce_stationarity=False,
                                 enforce_invertibility=False)

model_fit = model.fit()

pred=model_fit.predict(start='2019-01',end='2019-03')
print(mean_squared_error(test_y,pred))
print(test_y)
print(pred)
       