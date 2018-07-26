'''
Created on 23 Jul. 2018

@author: pengwang
'''

from datetime import datetime
import numpy as np
import pandas as pd
from jane.ImportExcel import ImportExcel

class JaneP(object):
    
    def __init__(self):
        self.mth=datetime.now().month
        ie=ImportExcel()
        ie.loadFiles()
        self.repos=ie.repos
    

    #create b19,f18a17,f18b18 rows. generate indexes[type,name]
    def generateRows(self):
        self.actualDf['type']='b18'
        self.actualDf=self.actualDf.set_index(['type','name'])
        self.budgetDf['type']='f18'
        self.budgetDf=self.budgetDf.set_index(['type','name'])
        self.priorDf['type']='a17'
        self.priorDf=self.priorDf.set_index(['type','name'])
        self.b19=pd.DataFrame().reindex_like(self.budgetDf).fillna(0).replace([np.inf,-np.inf],0)
        self.b19.rename(index={'f18':'b19'},inplace=True)
        
        #f18a17=(p-a)/a 
        self.f18a17=(self.priorDf.loc['a17']-self.actualDf.loc['b18']).div(self.actualDf.loc['b18']).fillna(0).replace([np.inf,-np.inf],0)
        self.f18a17['type']='f18VSa17'
        self.f18a17.reset_index(inplace=True)
        self.f18a17.set_index(['type','name'],inplace=True)
      
        #f18b18=(a-b)/b
        self.f18b18=(self.actualDf.loc['b18']-self.budgetDf.loc['f18']).div(self.budgetDf.loc['f18']).fillna(0).replace([np.inf,-np.inf],0)
        self.f18b18['type']='f18VSb18'
        self.f18b18.reset_index(inplace=True)
        self.f18b18.set_index(['type','name'],inplace=True)
        
        #b19f18
        self.b19f18=(self.b19.loc['b19']-self.budgetDf.loc['f18']).div(self.budgetDf.loc['f18']).fillna(0).replace([np.inf,-np.inf],0)
        self.b19f18['type']='b19VSf18'
        self.b19f18.reset_index(inplace=True)
        self.b19f18.set_index(['type','name'],inplace=True)
        
        self.depos=pd.DataFrame()
        self.depos=self.depos.append(self.priorDf)
        self.depos=self.depos.append(self.actualDf)
        self.depos=self.depos.append(self.budgetDf)
        self.depos=self.depos.append(self.b19)
        self.depos=self.depos.append(self.f18a17)
        self.depos=self.depos.append(self.f18b18)
        self.depos=self.depos.append(self.b19f18)     


    def main(self):

        #self.repreduceAccountsByAccountList()
        self.reduceRepositoryByAccounts()
        self.createRemainingCol()
        self.generateRows()   
        
if __name__ == "__main__":
    jan=JaneP()
    jan.main()


