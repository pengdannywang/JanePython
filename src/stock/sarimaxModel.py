import pandas as pd

import pandas_datareader.data as web 
import statsmodels.api as sm
import os
# SARIMAX example
from statsmodels.tsa.statespace.sarimax import SARIMAX

from sklearn.metrics import mean_squared_error


import matplotlib.pylab as plt
import itertools
import math
import warnings
import datetime
from datetime import timedelta
warnings.filterwarnings('ignore')

def measure_rmse(actual, predicted):
    return math.sqrt(mean_squared_error(actual, predicted))

def selectParameters(ticker,y,steps=3,disp=False):
    train_y, test_y = y[:-steps], y[-steps:]
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
    parameters=[]
    forcast=None
    for param in pdq:
        for t in trend_c:
            for param_seasonal in seasonal_pdq:
                try:
                    model = SARIMAX(train_y,
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

                    if parameters==[] or parameters[-1]>mse:
                        parameters=[ticker]+list(param)+list(param_seasonal)+[t]+[model_fit.aic]+[mse]
                        forcast=pred
                    
                except :

                    #print('ARIMA{} error:{}'.format(param,e))
                    error=error.append([list(param)+list(param_seasonal)+[t]],ignore_index=True)
                    pass
    print(parameters)
    #model_fit=model.fit(disp=0)
    if disp:
        print('forcast::',forcast)
        pred_ci=pd.DataFrame(index=forcast.index)
        pred_ci['low'] = forcast-forcast*0.05
        pred_ci['upper'] = forcast+forcast*0.05
        
     
        #pred_ci.loc[y.index[-1]]=[y[-1],y[-1]]
        #pred_ci=pred_ci.sort_index()
        ax = y['2019-01-01':].plot(label='observed')
        forcast.plot(ax=ax, label='Forecast', alpha=.7)
        
        ax.fill_between(forcast.index,
                        pred_ci.iloc[:,0],
                        pred_ci.iloc[:,1], color='k', alpha=.1)
        
        ax.set_xlabel('Date')
        ax.set_ylabel(ticker)
        plt.legend()
        
        plt.show()


    return parameters


def sarimaxPrdict(ticker,train_y,p_order,p_seasonal_order,trend,steps=1,disp=False,days=90):
    pred=None
    try:
        model = sm.tsa.statespace.SARIMAX(train_y,
                                             order=p_order,
                                             seasonal_order=p_seasonal_order,
                                             trend=trend,
                                             enforce_stationarity=False,
                                             enforce_invertibility=False)

        model_fit = model.fit(disp=False)

        pred=model_fit.forecast(steps=steps)
    except Exception as e: 
        print('sarimaxPrdict has a exception for:',ticker,p_order,p_seasonal_order,trend,steps,e,'return None')
        return None
    pred=train_y[-1:].append(pred)
    if disp:
        pred_ci=pd.DataFrame(index=pred.index)
        pred_ci['low'] = pred-pred*0.05
        pred_ci['upper'] = pred+pred*0.05
        
        end = datetime.date.today()
        delta=timedelta(days=days)
        
        chart_start_day=end-delta
        #pred_ci.loc[y.index[-1]]=[y[-1],y[-1]]
        #pred_ci=pred_ci.sort_index()
        ax = train_y[chart_start_day:].plot(label='observed')
        pred.plot(ax=ax, label='Forecast', alpha=.7)
        
        ax.fill_between(pred.index,
                        pred_ci.iloc[:,0],
                        pred_ci.iloc[:,1], color='k', alpha=.1)
        
        ax.set_xlabel('Date')
        ax.set_ylabel(ticker)
        plt.legend()
        
        plt.show()
    

    return pred
def dynamicForacast(ticker,y,steps=2,disp=False):
    paramPath='/root/pythondev/JanePython/parameters.csv'
    p1,p2,t=[],[],''
    result=None
    exists = os.path.isfile(paramPath)
    params=pd.DataFrame([],columns=['p1','p2','p3','p4','p5','p6','p7','trend','aic','mse'])
    if(exists):
        params=pd.read_csv(paramPath,index_col=0)
    try:
        parameters=selectParameters(ticker,y,steps=steps,disp=False)
        print('new calculated parameter:',parameters)
        if(len(parameters)>8):
            p1,p2,t=parameters[1:4],parameters[4:8],parameters[8]
 
        if not (p1==[] or p2==[] or t==''):
            result=sarimaxPrdict(ticker,y,p1,p2,t,steps=steps,disp=disp)
            params.loc[ticker]=parameters[1:]
            params.to_csv(paramPath) 
    except Exception as e: 
        print('unable to do prediction,recalculate parameter,',ticker, ' errors::',e)
        pass
        
    return result
def forcastStocks(paramPath,ticker,y,steps=2,disp=False):
    exists = os.path.isfile(paramPath)
    params=pd.DataFrame([],columns=['p1','p2','p3','p4','p5','p6','p7','trend','aic','mse'])
    if(exists):
        params=pd.read_csv(paramPath,index_col=0)
    
    p1,p2,t=[],[],''
    result=None
    if (len(params)>0 and params.index.contains(ticker)):
        li=params.loc[ticker].tolist()
        print(ticker,'exists in parameters:',li)
        p1,p2,t=li[0:3],li[3:7],li[7]
       
    else:
        parameters=selectParameters(ticker,y,steps=steps,disp=False)
        print('new calculated parameter:',parameters)
        if(len(parameters)>8):
            p1,p2,t=parameters[1:4],parameters[4:8],parameters[8]
            params.loc[ticker]=parameters[1:]
            params.to_csv(paramPath) 
            
    try: 
        if not (p1==[] or p2==[] or t==''):
            result=sarimaxPrdict(ticker,y,p1,p2,t,steps=steps,disp=disp)
    except Exception as e: 
        print('unable to do prediction,recalculate parameter,',ticker, ' errors::',e)
        try:
            parameters=selectParameters(ticker,y,steps=steps,disp=False)
            print('recalculated parameter:',parameters)
            if(len(parameters)>8):
                p1,p2,t=parameters[1:4],parameters[4:8],parameters[8]
                params.loc[ticker]=parameters[1:]
                params.to_csv(paramPath)  

                result=sarimaxPrdict(ticker,y,p1,p2,t,steps=steps,disp=disp)
            else:
                print('unable to forcast for ',ticker)
        except Exception as e: 
            print('fatal erros for ',ticker,'errors:',e)
    return result
def quickParameters(paramPath,ticker,y,steps=2,disp=False):
    exists = os.path.isfile(paramPath)
    params=pd.DataFrame([],columns=['p1','p2','p3','p4','p5','p6','p7','trend','aic','mse'])
    if(exists):
        params=pd.read_csv(paramPath,index_col=0)
    

    parameters=[]
    if (len(params)>0 and params.index.contains(ticker)):
        parameters=[ticker]+params.loc[ticker].tolist()
        print(ticker,'exists in parameters:',parameters)
        
       
    else:
        parameters=selectParameters(ticker,y,steps=steps,disp=False)
        print('new calculated parameter:',parameters)
        if(len(parameters)>8):
            params.loc[ticker]=parameters[1:]
            params.to_csv(paramPath) 
            
    return parameters


def predictbyticker(ticker,period='MS',months=18,steps=2,disp=False):
    end = datetime.date.today()
    day=end.day
    year=end.year-months//12-1
    month=months%12+1
    start=datetime.datetime(year,month,day)
    
    y=web.DataReader(ticker,"yahoo",start,end)['Adj Close']   
    y=y.resample(period).mean()
    parameters=selectParameters(ticker,y,steps=steps,disp=False)
    p1,p2,t=parameters[1:4],parameters[4:8],parameters[8]
    result=sarimaxPrdict(ticker,y,p1,p2,t,steps=steps,disp=disp)

    return result


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
result.to_csv(path+'/monthlypredicts.csv')

        
