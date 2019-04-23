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


import matplotlib.pylab as plt
import itertools
data=pd.read_csv('u:/python/test/computedStocks.csv',index_col=0)
stock=pd.read_csv('u:/python/test/stocks.csv',parse_dates=['Date'],index_col='Date')  
stock=stock.resample('MS').mean()
stock=stock.dropna(axis=1)
aa=stock.iloc[-1]
aa.name=str(aa.name.date())
data=data.append(aa)
data=data.sort_index()

