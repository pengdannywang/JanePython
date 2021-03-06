'''
Created on 24Jul.,2018

@author: pwang
'''
import unittest
from GoogleExcel import GoogleExcel
from JaneP import JaneP
import pandas as pd
import numpy as np


class Test(unittest.TestCase):


    def setUp(self):
        self.jan=JaneP()


    def tearDown(self):
        pass

    @unittest.skip
    def testName(self):
        self.assertTrue(len(self.io.budgetDf)>0, 'working ')
        self.assertTrue(len(self.io.repos)>0, 'working ')
        print(self.io.repos.count(level='name'))
        print(self.io.repos.loc['a17'].div(self.io.repos.loc['b18']))
    @unittest.skip
    def testSheetName(self):
        plds=self.io.loadTemplateWorkSheet('interface1')
        df=pd.DataFrame(columns=['accounts','parent','level','percentages','formula'])
        for i in range(1,len(plds)):
            row=[plds[i][0],plds[i][1],plds[i][2],plds[i][3],plds[i][4]]
            df.loc[len(df)]=row

        print(df)
        print(pd.unique(df['parent']))
        parents=pd.unique(df['parent'])
        for p in parents:
            if(p!=''):
                sub=df.query("parent=='"+p+"'")
                
                print(sub)
    @unittest.skip   
    def testCalculate(self):
        arr=['GROSS SALES - OG','FREIGHT - OG','DISCOUNTS - OG','NET SALES - OG']
        test=self.io.repos.query("name in "+str(arr))
        print("------testCalculate------")
        print(test)
        
    @unittest.skip
    def testShowHead(self):
        print(self.jan.pres.listHead(self.jan.repos))
        
    
    def testPresentationListRow(self):

        test=self.jan.writeBackSheet()
        
        
        
        print(test)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()