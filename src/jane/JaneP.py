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
        ie.loadFiles()
        self.rawPres=ie.loadPresentation('interface1')
        self.repos=ie.repos
        self.pres=Presentation()

    



        
if __name__ == "__main__":
    jan=JaneP()



