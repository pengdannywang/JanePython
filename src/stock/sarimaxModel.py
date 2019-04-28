import pandas as pd

from datetime import datetime

import statsmodels.api as sm

# SARIMAX example
from statsmodels.tsa.statespace.sarimax import SARIMAX

from sklearn.metrics import mean_squared_error


import matplotlib.pylab as plt
import itertools
import math
import warnings
start=datetime.now()
warnings.filterwarnings('ignore')

def measure_rmse(actual, predicted):
	return math.sqrt(mean_squared_error(actual, predicted))

def selectParameters(y,steps=3,disp=False):
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
                        parameters=list(param)+list(param_seasonal)+[t]+[model_fit.aic]+[mse]
                        forcast=pred
                    
                except :

                    #print('ARIMA{} error:{}'.format(param,e))
                    error=error.append([list(param)+list(param_seasonal)+[t]],ignore_index=True)

                    pass
    #model_fit=model.fit(disp=0)
    if disp:  

        print(parameters)
        pred_ci=pd.DataFrame(index=forcast.index)
        pred_ci['low'] = forcast-forcast*0.05
        pred_ci['upper'] = forcast+forcast*0.05
        
        
        #pred_ci.loc[y.index[-1]]=[y[-1],y[-1]]
        #pred_ci=pred_ci.sort_index()
        ax = y['2018':].plot(label='observed')
        forcast.plot(ax=ax, label='Forecast', alpha=.7)
        
        ax.fill_between(forcast.index,
                        pred_ci.iloc[:,0],
                        pred_ci.iloc[:,1], color='k', alpha=.1)
        
        ax.set_xlabel('Date')
        ax.set_ylabel(y.name)
        plt.legend()
        
        plt.show()
    p1,p2,t,err=parameters[0:3],parameters[3:7],parameters[7],parameters[-1]

    return p1,p2,t,err


def sarimaxPrdict(train_y,p_order,p_seasonal_order,trend,steps=1,disp=False):

    model = sm.tsa.statespace.SARIMAX(train_y,
                                         order=p_order,
                                         seasonal_order=p_seasonal_order,
                                         trend=trend,
                                         enforce_stationarity=False,
                                         enforce_invertibility=False)

    model_fit = model.fit(disp=False)

    pred=model_fit.forecast(steps=steps)
    if disp:
        pred_ci=pd.DataFrame(index=pred.index)
        pred_ci['low'] = pred-pred*0.05
        pred_ci['upper'] = pred+pred*0.05
        
        
        #pred_ci.loc[y.index[-1]]=[y[-1],y[-1]]
        #pred_ci=pred_ci.sort_index()
        ax = train_y['2018':].plot(label='observed')
        pred.plot(ax=ax, label='Forecast', alpha=.7)
        
        ax.fill_between(pred.index,
                        pred_ci.iloc[:,0],
                        pred_ci.iloc[:,1], color='k', alpha=.1)
        
        ax.set_xlabel('Date')
        ax.set_ylabel(train_y.name)
        plt.legend()
        
        plt.show()
    return pred

data=pd.read_csv('/Users/pengwang/work/stocks.csv',parse_dates=['Date'],index_col='Date')

data=data.resample('MS').mean()
y=data['ABBV']
start=datetime.now()
para=selectParameters(y,steps=3,disp=False)
end=datetime.now()
period=end-start

print('period:',period.seconds)

        
