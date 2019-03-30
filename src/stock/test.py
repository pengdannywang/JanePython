import pandas as pd
import pandas_datareader.data as web   # Package and modules for importing data; this code may change depending on pandas version
import datetime
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
data=pd.read_csv('u:/python/test/stocks.csv',parse_dates=['Date'],index_col='Date')

import matplotlib.pylab as plt
import itertools
    


res=data.resample('MS').mean()
y=res['AAL']
train_y,test_y=y[:-3],[y[-3:]]
# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
# fit model
model=ARIMA(train_y,order=(1,1,0))
#for param in pdq:
#    for param_seasonal in seasonal_pdq:
#        try:
#            model = sm.tsa.statespace.SARIMAX(train_y,
#                                 order=param,
#                                 seasonal_order=param_seasonal,
#                                 enforce_stationarity=False,
#                                 enforce_invertibility=False)
# 
#
#            model_fit = model.fit()
#            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, model_fit.aic))
#            pred=model_fit.predict(start='2019-01',end='2019-03')
#            print(pred)
#            print(test_y)
#        except:
#            continue
model_fit=model.fit(disp=0)
pred=model_fit.forecast(steps=3)
print(pred)
print(test_y)
            
ax = y.plot(label='observed', figsize=(20, 15))
pred.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred.index,
                pred.iloc[:, 0],
                pred.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('CO2 Levels')

plt.legend()
plt.show()
