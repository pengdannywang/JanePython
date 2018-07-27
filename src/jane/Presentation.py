'''
Created on 25 Jul. 2018

@author: pengwang
'''
import pandas as pd
import numpy as np
from jane.NormalizeRawData import COLINDEX as ci
class Presentation(object):
    
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
        parents=(presdf.query(ci.CONFIG_LEVEL+"=='"+str(level)+"'"))[ci.CONFIG_PARENT].unique()
        parents=list(filter(None,parents))
        return (parents)
    
    
    def getSumOfAParent(self,parent,configPresentation,presentation):
        accounts= configPresentation.query(ci.CONFIG_PARENT+"=='"+str(parent)+"'")
        sub=presentation[presentation[ci.INDEX_NAME].isin(accounts[ci.CONFIG_ACCOUNT])].sum(axis=0).tolist()
        sub[0]=parent
        
        return sub
    
    def getAllAccounts(self,configPresentation,repos):
        parents1=self.getParents(configPresentation,1)
        parents2=self.getParents(configPresentation,2)
        parents3=self.getParents(configPresentation,3)
        parents4=self.getParents(configPresentation,4)
        cols=[ci.INDEX_NAME]+ci.SORT_INDEXES*len(ci.COLUMNS_WITHOUT_INDEXES)
        presentation=pd.DataFrame(columns=cols)
        i=j=0
        for p in parents1:
            
            for i in range(0,len(configPresentation)):
                
    #             presentation.loc[i][0]=configPresentation[ci.CONFIG_ACCOUNT].loc[i]
               
                if(configPresentation[ci.CONFIG_PARENT].loc[i]==p ):
                    presentation.loc[len(presentation)]=self.listRow(configPresentation[ci.CONFIG_ACCOUNT].loc[i],repos)
                    
                
                if(~pd.isnull(p) and configPresentation[ci.CONFIG_ACCOUNT].loc[i]==p):  
                    presentation.loc[len(presentation)]=self.getSumOfAParent(p, configPresentation, presentation)
                    break
                
        for p in parents2:
            
            for i in range(0,len(configPresentation)):
                #presentation.loc[i][0]=configPresentation[ci.CONFIG_ACCOUNT].loc[i]
                if(~pd.isnull(p) and configPresentation[ci.CONFIG_ACCOUNT].loc[i]==p):  
                    presentation.loc[len(presentation)]=self.getSumOfAParent(p, configPresentation, presentation)
                    break
                
        for p in parents3:
            
            for i in range(0,len(configPresentation)):
                #presentation.loc[i][0]=configPresentation[ci.CONFIG_ACCOUNT].loc[i]
                if(~pd.isnull(p) and configPresentation[ci.CONFIG_ACCOUNT].loc[i]==p):  
                    presentation.loc[len(presentation)]=self.getSumOfAParent(p, configPresentation, presentation)
                    break
                
        for p in parents4:
            
            for i in range(0,len(configPresentation)):
                #presentation.loc[i][0]=configPresentation[ci.CONFIG_ACCOUNT].loc[i]
                if(~pd.isnull(p) and configPresentation[ci.CONFIG_ACCOUNT].loc[i]==p):  
                    presentation.loc[len(presentation)]=self.getSumOfAParent(p, configPresentation, presentation)
                    break             
        return presentation   
#         for a in accounts:
            
    
    
    