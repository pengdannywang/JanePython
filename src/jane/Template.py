'''
Created on 25 Jul. 2018

@author: pengwang
'''
import pandas as pd
import numpy as np
from jane.NormalizeRawData import COLINDEX as ci

class Template(object):
    
    def __init__(self):
        '''
        Constructor
        '''
    def listHead(self,data):
        head=data.columns
        head2=data.index.levels[0].tolist()
        return(head,head2)
    
      
    def listRow(self,accountName,data):
        value=[accountName]
        for col in data.columns:
            value.extend(data.query(ci.INDEX_NAME+"=='"+accountName+"'")[col].tolist())
            
        return value
    
    
    def getParents(self,presdf,level):
        parents=(presdf.query(ci.CONFIG_LEVEL+"=="+str(level)))[ci.CONFIG_ACCOUNT].unique()
        parents=list(filter(None,parents))
        return (parents)
    
    
    def getSumOfAParent(self,parent,templateSheet,outputData):
        accounts= templateSheet.query(ci.CONFIG_PARENT+"=='"+str(parent)+"'")
        sub=outputData[outputData[ci.INDEX_NAME].isin(accounts[ci.CONFIG_ACCOUNT])].sum(axis=0).tolist()
        sub[0]=parent
        
        return sub
        
    def getPercentages(self,name,numerator,denominator,outputData):
        
        num=outputData[outputData[ci.INDEX_NAME]==numerator].loc[:,outputData.columns!=ci.INDEX_NAME]
        den=outputData[outputData[ci.INDEX_NAME]==denominator].loc[:,outputData.columns!=ci.INDEX_NAME]
        num.reset_index(inplace=True,drop=True)
        den.reset_index(inplace=True,drop=True)
        sub=num.div(den).fillna(0).replace([np.inf,-np.inf],0)
        col=pd.DataFrame({ci.INDEX_NAME:[name]})
        
        result=pd.concat([col,sub],axis=1,sort=False)
        

        
        return result
    def getDataWithTemplateOrder(self,templateSheet,repos):
        
        parents1=self.getParents(templateSheet,2)
        parents2=self.getParents(templateSheet,3)
        parents3=self.getParents(templateSheet,4)
        parents4=self.getParents(templateSheet,5)
        cols=[ci.INDEX_NAME]+ci.SORT_INDEXES*len(ci.COLUMNS_WITHOUT_INDEXES)
        pre_value=pd.DataFrame(columns=cols)


        for i in range(0,len(templateSheet)):
#             pre_value.loc[i][0]=templateSheet[ci.CONFIG_ACCOUNT].loc[i]
            print(self.listRow(templateSheet[ci.CONFIG_ACCOUNT].loc[i],repos))
            if(templateSheet[ci.CONFIG_LEVEL].loc[i]==1): 
                pre_value.loc[len(pre_value)]=self.listRow(templateSheet[ci.CONFIG_ACCOUNT].loc[i],repos)

                
        for p in parents1:
            if(~pd.isnull(p) and templateSheet[ci.CONFIG_ACCOUNT].loc[i]==p):  
                pre_value.loc[len(pre_value)]=self.getSumOfAParent(p, templateSheet, pre_value)

        for p in parents2:
            if(~pd.isnull(p) and templateSheet[ci.CONFIG_ACCOUNT].loc[i]==p):  
                pre_value.loc[len(pre_value)]=self.getSumOfAParent(p, templateSheet, pre_value)
        for p in parents3:
            if(~pd.isnull(p) and templateSheet[ci.CONFIG_ACCOUNT].loc[i]==p):  
                pre_value.loc[len(pre_value)]=self.getSumOfAParent(p, templateSheet, pre_value)
                
        for p in parents4:
            if(~pd.isnull(p) and templateSheet[ci.CONFIG_ACCOUNT].loc[i]==p):  
                pre_value.loc[len(pre_value)]=self.getSumOfAParent(p, templateSheet, pre_value)

#         percent=templateSheet.query(ci.CONFIG_LEVEL+"=='10'")
#         percent=percent.reset_index()
#         for i in range(0,len(percent)):
#  
#             row=self.getPercentages(percent[ci.CONFIG_ACCOUNT].loc[i],percent[ci.CONFIG_PRECENTAGES].loc[i], percent[ci.CONFIG_DENOMINATOR].loc[i], pre_value)
#             pre_value=pre_value.append(row,ignore_index=True)       
            
        return pre_value
#         for a in accounts:
            
    
    