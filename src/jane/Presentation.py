'''
Created on 25 Jul. 2018

@author: pengwang
'''
import pandas as pd
import numpy as np

class Presentation(object):
    '''
    classdocs
    '''


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
    
        parents=pd.unique(presdf['parent'])
        return (parents)
    
    def getSubByAParent(self,parent,presentation):
        return presentation.query("parent=='"+parent+"'")
    
    