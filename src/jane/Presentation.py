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
    
      
    def listRow(self,col,accountName,data):
        return data.query("name=='"+accountName+"'")[col].tolist()
    
        
    def getParents(self,presdf):
        parents=pd.unique(presdf[ci.CONFIG_PARENT])
        return (parents)
    
    
    def getSubByAParent(self,parent,presentation):
        return presentation.query(ci.CONFIG_PARENT+"=='"+parent+"'")
    
    def getAllAccounts(self,rawPres):
        accounts=rawPres[ci.CONFIG_ACCOUNT]
        cols=[ci.INDEX_NAME]+ci.INDEX_NAME,ci.SORT_INDEXES*len(ci.COLUMNS_WITHOUT_INDEXES)
        presentation=pd.DataFrame(columns=cols)
        presentation.loc[len(presentation)]=0
#         for a in accounts:
            
    
    
    