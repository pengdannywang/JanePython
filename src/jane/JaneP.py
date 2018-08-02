'''
Created on 23 Jul. 2018

@author: pengwang
'''

from datetime import datetime
import numpy as np
import pandas as pd
import sys, getopt
from jane.MicroExcel import MicroExcel
from jane.ImportExcel import ImportExcel
from jane.Presentation import Presentation

class JaneP(object):
    
    def __init__(self):
        self.mth=datetime.now().month
        
        
        self.presentationName='interface1'
        
        self.pres=Presentation()
        # pres.getAllAccounts(configPresentation, self.repos)
        self.google_cres="E:/downloads/JaneProject-f472d80e0028.json"
        self.google=False
        self.fileName='U:/tools/jane/entityConfig.xlsx'
        self.outputName='sheet'
    def doProcess(self):
        if(self.google):
            self.ie=ImportExcel()
        else:
            self.ie=MicroExcel()
        self.ie.loadSheet(self.fileName)
        self.repos=self.ie.repos
        self.configPresentation=self.ie.loadPresentation(self.presentationName)
        self.prestationData=self.pres.getAllAccounts(self.configPresentation, self.repos)
        sheet= self.ie.getSheet(self.outputName)
        self.ie.writeToSheet(sheet, self.prestationData, self.configPresentation)
        
    def main(self,argv):
        
        if argv == []:
            print("Usage: " + sys.argv[0] + " -h for help")
            return
        try:
            # opts, args = getopt.getopt(argv,"hf:o:",["ifile=","ofile="])
            opts, args = getopt.getopt(argv, "hg:f:p:o:", ["help","google Drive","file=","presentation=","output="])
        except getopt.GetoptError:
            print("Usage: " + sys.argv[0] + " -h for help")
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('Syntax: ' + sys.argv[0] + ' \n\n -h help.\n -g google Drive. \n -f file path and name.\n  -p presentation name.\n -o output path and file name.\n')
                sys.exit()
            elif opt in ("-g", "-google"):
                self.google=True
                self.google_cres=arg
            elif opt in ("-f","-file"):
                self.fileName=arg
            elif opt in ("-p","-presentation"):
                self.presentationName=arg.lower()
            elif opt in ("-o","-output"):
                self.outputName=arg
        
        self.doProcess()

if __name__ == "__main__":
    jan=JaneP()
    jan.main(sys.argv[1:])


