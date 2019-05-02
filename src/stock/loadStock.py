import pandas as pd
import pandas_datareader.data as web   # Package and modules for importing data; this code may change depending on pandas version
import datetime
import numpy as np

import random
import statsmodels.api as sm
# SARIMAX example
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sarimaxModel import selectParameters
from sarimaxModel import sarimaxPrdict

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2016,1,1)
end = datetime.date.today()
result=pd.DataFrame()
name='BHP'
res=web.DataReader(name,"yahoo",start,end)['Adj Close']
res.name=name
y=res.resample('MS').mean()

p1,p2,t,err=selectParameters(y,steps=3,disp=True)
pred=sarimaxPrdict(y,p1,p2,t,steps=3,disp=True)

