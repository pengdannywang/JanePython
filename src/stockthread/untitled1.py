from sarimaxModel import predictbyticker
import pandas as pd
from datetime import timedelta
import statsmodels.api as sm
import pandas_datareader.data as web
import datetime
from sarimaxModel import selectParameters
from sarimaxModel import sarimaxPrdict
#data=pd.read_csv('/Users/pengwang/work/stocks.csv',parse_dates=['Date'],index_col='Date')

end = datetime.date.today()
months=18
ticker='MFG.AX'
day=end.day
year=end.year-months//12-1
month=months%12+1
start=datetime.datetime(year,month,day)
data=web.DataReader(ticker,"yahoo",start,end)['Adj Close']
y=data.resample('W').mean()
y=data['2018-04-01':]
#parameters=selectParameters(ticker,y,steps=3,disp=True)
parameters=['MFG.AX', 0, 1, 0, 0, 0, 0, 12, 'n', 39.92467376324733, 0.10954492938239571]
p1,p2,t=parameters[1:4],parameters[4:8],parameters[8]

result=sarimaxPrdict(ticker,y,p1,p2,t,steps=3,disp=True)