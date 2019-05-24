import pandas as pd
from sarimaxModel import dynamicForacast


path='/root/pythondev/JanePython/'
inputfile = path+'Yahoo.xlsx'
outputfile = 'stocks2.csv'

savepath=path+outputfile
stocks=pd.read_csv(savepath,parse_dates=['Date'],index_col='Date')
data=stocks.resample('MS').mean()
result=pd.DataFrame()
for ticker in data.columns:
    print(ticker)
    res=dynamicForacast(ticker,data[ticker])
    if(res is not None):
        result[ticker]=res
#dd=pd.DataFrame()        
#sres=result.transpose().sort_values(by='2019-06-01',ascending=False)
#rate=sres['2019-07-01']/sres['2019-05-01'] 
#x=rate*1000-1000
#dd['benefit']=x
#dd['rate']=rate
#dd['2019-05-01']=sres['2019-05-01']
#dd['2019-06-01']=sres['2019-06-01']
#dd['2019-07-01']=sres['2019-07-01']
#dd.sort_values(by='benefit',ascending=False).head(30)
result.to_csv(path+'/weeklyforecast.csv')