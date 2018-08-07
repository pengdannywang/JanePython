import quandl
import numpy as np
quandl.ApiConfig.api_key ='PQoMLmKGuFsMHQJDbXSJ'
#quandl.ApiConfig.api_key = 'PQoMLmKGuFsMHQJDbXSJ'
mydata=quandl.get('EOD/AAPL')
#mydata =quandl.bulkdownload("ZEA")
print(mydata['Adj_Close'])
