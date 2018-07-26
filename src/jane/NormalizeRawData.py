'''
Created on 24Jul.,2018

@author: pwang
'''
from datetime import datetime
import re

import numpy as np
import pandas as pd
from json.decoder import NaN


def normalize(typeName,rawData):
    data=convertListListToDf(rawData)
    data=removeEmptyRow(data)
    data= createRemainingCol(data)
    data.drop_duplicates(subset='name', keep='first', inplace=True)
    data=setIndexesByTypeAndName(typeName, data)
    return data            
#create columns: "1 to month" "month to 12","monthly average","1st quarter" -"4th quarter"
def createRemainingCol(rawDf):
    mth=datetime.now().month
    rawDf['Total']=rawDf.sum(axis=1)

    position=mth+1
    # add column '1 To current Month'
    colName="1 to "+str(mth)
    rawDf[colName]=rawDf.iloc[:,1:position].sum(axis=1)

    #add column 'next Month to 12
    colName=str(mth+1) +" To 12"
    rawDf[colName]=rawDf.iloc[:,position:13].sum(axis=1)

    
    colName="monthly average"
    rawDf[colName]=rawDf.mean(axis=1)

    colName="1ST QUARTER"
    rawDf[colName]=rawDf.iloc[:,1:4].sum(axis=1)

    colName="2ND QUARTER"
    rawDf[colName]=rawDf.iloc[:,4:7].sum(axis=1)

    colName="3RD QUARTER"
    rawDf[colName]=rawDf.iloc[:,7:10].sum(axis=1)

    colName="4ST QUARTER"
    rawDf[colName]=rawDf.iloc[:,10:13].sum(axis=1)
    return rawDf

    
def convertListListToDf(data):
    arr=pd.DataFrame(columns=["name","01","02","03","04","05","06","07","08","09","10","11","12"])
    for i in range(len(data)):
        cname=data[i][0]
        if(validStr(cname)):
            m=[cname]
            for j in range(1,13):
                mth=convertToNum(data[i][j])
                m.append(mth)
            if(validateList(m)):
                arr.loc[len(arr)]=m
    
    return arr


def setIndexesByTypeAndName(typeName,rawData):
    
    rawData['type']=typeName
    data=rawData.set_index(['type','name'])
    return data
    #isin(x) x must be a list or array. using df.columnName to get a list 
    #    


def generateB19(data):
        b19=pd.DataFrame().reindex_like(data).fillna(0).replace([np.inf,-np.inf],0)
        typeName=data.index.get_level_values('type')[1]
        b19.rename(index={typeName:'b19'},inplace=True)
        return b19

    
def reduceRepositoryByAccounts(data,accountList):
    data=data.loc[data.index.levels[1].isin(accountList['accountsName'])]
    typeName=data.index.levels[0][0]
    temp=accountList[ ~accountList['accountsName'].isin(data.index.levels[1].tolist())]
    lv1=np.repeat(typeName,len(temp)).tolist()
    lv2=temp['accountsName'].tolist()
    ts=list(zip(lv1,lv2))
    mindx=pd.MultiIndex.from_tuples(ts, names=['type','name'])
    rows=pd.DataFrame(columns=data.columns,index=mindx).fillna(0)
    data=data.append(rows)
    return data         
            
def validateList(row):
    validated=True
    name=row[0]
    jan=row[1]
    feb=row[2]
    mar=row[3]
    apr=row[4]
    may=row[5]
    jun=row[6]
    jul=row[7]
    aug=row[8]
    sep=row[9]
    octo=row[10]
    nov=row[11]
    dec=row[12]
    if(not validStr(name)):
        validated=False
    if(not validNumber(jan)):
        validated=False
    if(not validNumber(feb)):
        validated=False
    if(not validNumber(mar)):
        validated=False
    if(not validNumber(apr)):
        validated=False
    if(not validNumber(may)):
        validated=False
    if(not validNumber(jun)):
        validated=False
    if(not validNumber(jul)):
        validated=False
    if(not validNumber(aug)):
        validated=False
    if(not validNumber(sep)):
        validated=False
    if(not validNumber(octo)):
        validated=False
    if(not validNumber(nov)):
        validated=False
    if(not validNumber(dec)):
        validated=False
    return validated


def removeEmptyRow(df):
    df= df[df['01']!=0 ]
    df=df[df.name!='Currency: AUD']
    df=df[df.name!='name']
    return df

    
def validNumber(num):
    num=str(num)
    validated=False
    rx = re.compile('[^0-9eE.]')
    sub=rx.sub('',num)
    if(num==''):
        validated=True
    elif(len(sub)>0):
        validated=True
    return validated


def convertToNum(strNum):
    rx = re.compile('[^0-9.]')
    sub=rx.sub('',str(strNum))
    if(sub!=''):
        sub=float(sub)
    else:
        sub=0
    return sub


def validStr(str1):
    validated=False
    if(str1!=''):
        validated=True
    return validated


def adjustAccountList(accountList):

    accounts=pd.DataFrame(accountList,columns=['accountsName'])
    accounts.replace('',np.NaN,inplace=True)
    accounts=accounts.dropna(axis=0)
    accounts=accounts.drop(index=0,axis=0)
    return accounts
#create b19,f18a17,f18b18 rows. generate indexes[type,name]
def generatef18a17(data):
    
    #f18a17=(p-a)/a 
    f18a17=(data.loc['a17']-data.loc['b18']).div(data.loc['b18']).fillna(0).replace([np.inf,-np.inf],0)*100
    f18a17['type']='f18VSa17'
    f18a17.reset_index(inplace=True)
    f18a17.set_index(['type','name'],inplace=True)
    return f18a17

def generatef18b18(data):
    #f18b18=(a-b)/b
    f18b18=(data.loc['b18']-data.loc['f18']).div(data.loc['f18']).fillna(0).replace([np.inf,-np.inf],0)
    f18b18['type']='f18VSb18'
    f18b18.reset_index(inplace=True)
    f18b18.set_index(['type','name'],inplace=True)
    return f18b18

def generateb19f18(data):
    #b19f18
    b19f18=(data.loc['b19']-data.loc['f18']).div(data.loc['f18']).fillna(0).replace([np.inf,-np.inf],0)
    b19f18['type']='b19VSf18'
    b19f18.reset_index(inplace=True)
    b19f18.set_index(['type','name'],inplace=True)
    return b19f18
   
