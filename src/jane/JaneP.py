'''
Created on 23 Jul. 2018

@author: pengwang
'''

from datetime import datetime

import sys, getopt
from jane.MicroExcel import MicroExcel
from jane.GoogleExcel import GoogleExcel
from jane.Template import Template

class JaneP(object):
    
    def __init__(self):
        self.mth=datetime.now().month
        
        
        self.sheetName='interface1'
        
        self.pres=Template()
        # pres.getAllAccounts(template, self.repos)
        self.google_cres="/Users/pengwang/Downloads/JaneProject-614aeb27e1fc.json"
        self.google=False
        self.fileName='/Users/pengwang/Downloads/entityConfig.xlsx'
        self.outputFile='/Users/pengwang/Downloads/report.xlsx'

        
    def doProcess(self):
        if(self.google):
            self.io=GoogleExcel()
            self.io.loadSheet(self.google_cres)
        else:
            self.io=MicroExcel()
            self.io.loadSheet(self.fileName)
        self.repos=self.io.repos
        self.template=self.io.loadTemplate(self.sheetName)
        self.outputData=self.pres.getAllAccounts(self.template, self.repos)
        
        self.io.writeToSheet( self.outputFile,self.sheetName,self.outputData, self.template)
        
    def main(self,argv):
        
        #if argv == []:
        #   print("Usage: " + sys.argv[0] + " -h for help")
            #return
        try:
            # opts, args = getopt.getopt(argv,"hf:o:",["ifile=","ofile="])
            opts, args = getopt.getopt(argv, "hgf:t:o:", ["help","google Drive","file=","template=","output="])
        except getopt.GetoptError:
            print("Usage: " + sys.argv[0] + " -h for help")
            #sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('Syntax: ' + sys.argv[0] + ' \n\n -h help.\n -g google Drive. cres Path and Name \n -f file path and name.\n  -p presentation name.\n -o output path and file name.\n')
                sys.exit()
            elif opt in ("-g", "-google"):
                self.google=True
                #self.google_cres=arg
            elif opt in ("-f","-file"):
                self.io.fileName=arg
            elif opt in ("-t","-template"):
                self.io.sheetName=arg.lower()
            elif opt in ("-o","-output"):
                self.io.outputName=arg
            
        self.doProcess()

if __name__ == "__main__":
    jan=JaneP()
    jan.main(sys.argv[1:])


