
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import is_list_like
pd.core.common.is_list_like = is_list_like
import pandas_datareader as web
import datetime
# We will look at stock prices over the past year, starting at January 1, 2016
start = datetime.datetime(2018,1,1)
end = datetime.date.today()
 
# Let's get Apple stock data; Apple's ticker symbol is AAPL
# First argument is the series we want, second is the source ("yahoo" for Yahoo! Finance), third is the start date, fourth is the end date
apple = web.DataReader("AAPL", start, end)
 
type(apple)
print(apple)