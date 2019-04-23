import pandas as pd
import pandas_datareader.data as web   # Package and modules for importing data; this code may change depending on pandas version
import datetime
import numpy as np

import random
import statsmodels.api as sm
# SARIMAX example
from statsmodels.tsa.statespace.sarimax import SARIMAX

# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2016,1,1)
end = datetime.date.today()

res=web.DataReader('MMM',"yahoo",start,end)['Adj Close']