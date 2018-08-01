'''
Created on 23 Jul. 2018

@author: pengwang
'''

from datetime import datetime
import numpy as np
import pandas as pd
from jane.ImportExcel import ImportExcel
from jane.Presentation import Presentation

class JaneP(object):
    
    def __init__(self):
        self.mth=datetime.now().month
        self.ie=ImportExcel()
        self.repos=self.ie.repos
        self.configPresentation=self.ie.loadPresentation('interface1')
        self.pres=Presentation()
        # pres.getAllAccounts(configPresentation, self.repos)
        self.prestationData=self.pres.getAllAccounts(self.configPresentation, self.repos)

    def writeBackSheet(self):
        sheet= self.ie.getSheet("Sheet4")
        self.ie.writeToSheet(sheet, self.prestationData, self.configPresentation)
        
if __name__ == "__main__":
    jan=JaneP()



