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
        ie=ImportExcel()
        self.repos=ie.repos
        configPresentation=ie.loadPresentation('interface1')
        pres=Presentation()
       # pres.getAllAccounts(configPresentation, self.repos)
        self.prestationData=pres.getAllAccounts(configPresentation, self.repos)



        
if __name__ == "__main__":
    jan=JaneP()



