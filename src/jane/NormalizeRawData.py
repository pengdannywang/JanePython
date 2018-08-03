'''
Created on 24Jul.,2018

@author: pwang
'''
from datetime import datetime
import re
import numpy as np
import pandas as pd


class COLINDEX:
    mth=datetime.now().month
    NEXT_MONTH_NUM=mth+1
    INDEX_A17 = 'A17'
    INDEX_B18 = 'B18'
    INDEX_F18 = 'F18'
    INDEX_B19 = 'B19'
    INDEX_F18VSB18 = 'F18 vs. B18'
    INDEX_B19VSF18 = 'B19 vs. F18'
    INDEX_F18VSA17 = 'F18 vs. A17'
    INDEX_TYPE = 'type'
    INDEX_NAME = 'name'
    INDEX_PERCENTAGES=[INDEX_F18VSA17,INDEX_F18VSB18,INDEX_B19VSF18]
    SORT_INDEXES= [INDEX_A17,INDEX_F18,INDEX_B18,INDEX_B19]+INDEX_PERCENTAGES
    
    
    jan="Jan"
    FEB="Feb"
    MAR="Mar"
    APR="Apr"
    MAY="May"
    JUN="Jun"
    JUL="Jul"
    AUG="Aug"
    SEP="Sep"
    OCT="Oct"
    NOV="Nov"
    DEC="Dec"
    COL_TOTAL = 'Total'
    COL_MONTHLYAVERAGE = "Monthly Average"
    COL_PAST_OF_YEAR="1 to "+str(mth)
    COL_FUTURE_OF_YEAR=str(datetime.now().month+1)+" To 12"
    COL_SPRING = "1ST Quarter"
    COL_SUMMER="2ND Quarter"
    COL_AUTUMN="3RD Quarter"
    COL_WINTER="4ST Quarter"
    ACCOUNT_NAME = 'accountsName'

    COLUMNS_INITIAL=[INDEX_NAME,jan,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC]
    COLUMNS_WITHOUT_INDEXES=[jan,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC,COL_TOTAL,COL_PAST_OF_YEAR,COL_FUTURE_OF_YEAR,COL_MONTHLYAVERAGE,COL_SPRING,COL_SUMMER,COL_AUTUMN,COL_WINTER]
    
    COLUMNS_ALL=[INDEX_TYPE,INDEX_NAME]+COLUMNS_WITHOUT_INDEXES
    
    CONFIG_ACCOUNT='accounts'
    CONFIG_PARENT='parent'
    CONFIG_LEVEL='level'
    CONFIG_PRECENTAGES='percentages'
    CONFIG_DENOMINATOR='denominator'
    CONFIG_FORMULA='formula'
    CONFIG_COLUMNS=[CONFIG_ACCOUNT,CONFIG_PARENT,CONFIG_LEVEL,CONFIG_PRECENTAGES,CONFIG_DENOMINATOR,CONFIG_FORMULA]



def normalize(typeName,rawData):
    data=convertListListToDf(rawData)
    data=removeEmptyRow(data)
    data.drop_duplicates(subset=COLINDEX.INDEX_NAME, keep='first', inplace=True)
    data= createRemainingCol(data)
    
    data=setIndexesByTypeAndName(typeName, data)
    return data      

def normalizeExcel(typeName,cells):
    data=getDataFromCells(cells)
    data=removeEmptyRow(data)
    data.drop_duplicates(subset=COLINDEX.INDEX_NAME, keep='first', inplace=True)
    data= createRemainingCol(data)
    data=setIndexesByTypeAndName(typeName, data)
    return data   
       
#create columns: "1 to month" "month to 12","monthly average","1st quarter" -"4th quarter"
def createRemainingCol(rawDf):  
    rawDf[COLINDEX.COL_TOTAL]=rawDf.sum(axis=1)
    # add column '1 To current Month'
    rawDf[COLINDEX.COL_PAST_OF_YEAR]=rawDf.iloc[:,1:COLINDEX.NEXT_MONTH_NUM].sum(axis=1)
    #add column 'next Month to 12
    rawDf[COLINDEX.COL_FUTURE_OF_YEAR]=rawDf.iloc[:,COLINDEX.NEXT_MONTH_NUM:13].sum(axis=1)
    rawDf[COLINDEX.COL_MONTHLYAVERAGE]=rawDf.mean(axis=1)
    rawDf[COLINDEX.COL_SPRING]=rawDf.iloc[:,1:4].sum(axis=1)
    rawDf[COLINDEX.COL_SUMMER]=rawDf.iloc[:,4:7].sum(axis=1)
    rawDf[COLINDEX.COL_AUTUMN]=rawDf.iloc[:,7:10].sum(axis=1)
    rawDf[COLINDEX.COL_WINTER]=rawDf.iloc[:,10:13].sum(axis=1)
    return rawDf

    
def convertListListToDf(data):
    arr=pd.DataFrame(columns=COLINDEX.COLUMNS_INITIAL)
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

    
def getDataFromCells(cells):
    arr=pd.DataFrame(columns=COLINDEX.COLUMNS_INITIAL)
    for i in range(len(cells)):
            if(pd.isnull(cells[i][0].value)!=True and len(cells[i][0].value)>0):
                if(validateList(cells[i])):
                    acc=[cells[i][0].value]
                    for j in range(1,13):
                        mth=convertToNum(cells[i][j].value)
                        acc.append(mth)
                    arr.loc[len(arr)]=acc
    return arr

def setIndexesByTypeAndName(typeName,rawData):
    rawData[COLINDEX.INDEX_TYPE]=typeName
    data=rawData.set_index([COLINDEX.INDEX_TYPE,COLINDEX.INDEX_NAME])
    return data
    #isin(x) x must be a list or array. using df.columnName to get a list 
    #    


def generateB19(data):
    b19=pd.DataFrame().reindex_like(data).fillna(0).replace([np.inf,-np.inf],0)
    typeName=data.index.get_level_values(COLINDEX.INDEX_TYPE)[1]
    b19.rename(index={typeName:COLINDEX.INDEX_B19},inplace=True)

    return b19

    
def reduceRepositoryByAccounts(data,accountList):
    
    data=data.loc[data.index.levels[1].isin(accountList[COLINDEX.ACCOUNT_NAME])]
    index_type=data.index.levels[0][0]
    temp=accountList[~accountList[COLINDEX.ACCOUNT_NAME].isin(data.index.levels[1].tolist())]
    lv1=np.repeat(index_type,len(temp)).tolist()
    lv2=temp[COLINDEX.ACCOUNT_NAME].tolist()
    tupleIndex=list(zip(lv1,lv2))
    multiIndex=pd.MultiIndex.from_tuples(tupleIndex, names=[COLINDEX.INDEX_TYPE,COLINDEX.INDEX_NAME])
    rows=pd.DataFrame(columns=data.columns,index=multiIndex).fillna(0)
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
    df= df[df[COLINDEX.jan]!=0 ]
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


def removeEmptyRowForAccountList(accountList):
 
    accounts=pd.DataFrame(accountList,columns=[COLINDEX.ACCOUNT_NAME])
    accounts.replace('',np.NaN,inplace=True)
    #drop na row
    accounts=accounts.dropna(axis=0)
    #drop first name
    accounts=accounts.drop(index=0,axis=0)
    return accounts

def leanupExcelAccountTupleCells(accountTuples):
    accounts=pd.DataFrame(columns=[COLINDEX.ACCOUNT_NAME])
    for i in range(len(accountTuples)):
        if(pd.isnull(accountTuples[i][0].value)!=True):
            accounts.loc[len(accounts)]=accountTuples[i][0].value
    
    return accounts

#create INDEX_B19,f18a17,f18b18 rows. generate indexes[type,INDEX_NAME]
def generatef18a17(data):
    #f18a17=(p-a)/a 
    f18a17=(data.loc[COLINDEX.INDEX_A17]-data.loc[COLINDEX.INDEX_B18]).div(data.loc[COLINDEX.INDEX_B18]).fillna(0).replace([np.inf,-np.inf],0)
    f18a17[COLINDEX.INDEX_TYPE]=COLINDEX.INDEX_F18VSA17
    f18a17.reset_index(inplace=True)
    f18a17.set_index([COLINDEX.INDEX_TYPE,COLINDEX.INDEX_NAME],inplace=True)
    return f18a17


def generatef18b18(data):
    #f18b18=(a-b)/b
    f18b18=(data.loc[COLINDEX.INDEX_B18]-data.loc[COLINDEX.INDEX_F18]).div(data.loc[COLINDEX.INDEX_F18]).fillna(0).replace([np.inf,-np.inf],0)
    f18b18[COLINDEX.INDEX_TYPE]=COLINDEX.INDEX_F18VSB18
    f18b18.reset_index(inplace=True)
    f18b18.set_index([COLINDEX.INDEX_TYPE,COLINDEX.INDEX_NAME],inplace=True)
    return f18b18


def generateb19f18(data):
    #b19f18  
    b19f18=(data.loc[COLINDEX.INDEX_B19]-data.loc[COLINDEX.INDEX_F18]).div(data.loc[COLINDEX.INDEX_F18]).fillna(0).replace([np.inf,-np.inf],0)
    b19f18[COLINDEX.INDEX_TYPE]=COLINDEX.INDEX_B19VSF18
    b19f18.reset_index(inplace=True)
    b19f18.set_index([COLINDEX.INDEX_TYPE,COLINDEX.INDEX_NAME],inplace=True)
    return b19f18
   
