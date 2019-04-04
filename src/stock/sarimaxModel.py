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
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.stattools import adfuller
data=pd.read_csv('u:/python/test/stocks.csv',parse_dates=['Date'],index_col='Date')

import matplotlib.pylab as plt
import itertools
import math


def measure_rmse(actual, predicted):
	return math.sqrt(mean_squared_error(actual, predicted))

def selectParameters(y,test_y):
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
                    print([list(param)+list(param_seasonal)+[t]+[model_fit.aic]+[mse]])
                except :

                    #print('ARIMA{} error:{}'.format(param,e))
                    error=error.append([list(param)+list(param_seasonal)+[t]],ignore_index=True)
                    print(['error']+[list(param)+list(param_seasonal)+[t]])
                    pass
    #model_fit=model.fit(disp=0)
    mses=mses.sort_values(mses.columns[-1])
    print(mses)
    para=mses[0:1].values
    return para


def sarimaxPrdict(train_y,test_y,start=None,end=None):
    if(start==None):
        start=str(test_y.index[0].date())
    if(end==None):
        end=str(test_y.index[-1].date())
    #para=[[0, 1, 2, 0, 0, 0, 12, 'c', 130.56524060691842,0.1542178000703068]]

    para=selectParameters(train_y,test_y)
    print(para)
    t=para[0][7]
    para=[int(x) for x in para[0][0:7]]

    param=list(para[0:3])
    ps=list(para[3:7])


    model = sm.tsa.statespace.SARIMAX(train_y,
                                         order=param,
                                         seasonal_order=ps,
                                         trend=t,
                                         enforce_stationarity=False,
                                         enforce_invertibility=False)

    model_fit = model.fit(disp=False)
    print(start+' '+end)
    pred=model_fit.get_prediction(start=start,end=end, dynamic=False)

    return pred
#B         business day frequency
#C         custom business day frequency (experimental)
#D         calendar day frequency
#W         weekly frequency
#M         month end frequency
#SM        semi-month end frequency (15th and end of month)
#BM        business month end frequency
#CBM       custom business month end frequency
#MS        month start frequency
#SMS       semi-month start frequency (1st and 15th)
#BMS       business month start frequency
#CBMS      custom business month start frequency
#Q         quarter end frequency
#BQ        business quarter endfrequency
#QS        quarter start frequency
#BQS       business quarter start frequency
#A         year end frequency
#BA, BY    business year end frequency
#AS, YS    year start frequency
#BAS, BYS  business year start frequency
#BH        business hour frequency
#H         hourly frequency
#T, min    minutely frequency
#S         secondly frequency
#L, ms     milliseconds
#U         microseconds
#N, us     nanoseconds
res=data.resample('W').mean()

y=res['GOOGL']
train_y,test_y=y[:-6],y[-6:]
pred=sarimaxPrdict(train_y,test_y,start='2019-03',end='2019-05')

pred_ci = pred.conf_int()

#pred_ci.loc[y.index[-1]]=[y[-1],y[-1]]
#pred_ci=pred_ci.sort_index()
ax = y['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='Forecast', alpha=.7)

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.1)

ax.set_xlabel('Date')
ax.set_ylabel('CO2 Levels')
plt.legend()

plt.show()

