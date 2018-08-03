'''
Created on 23 Jul. 2018

@author: pengwang
'''

from datetime import datetime

import sys, getopt
from jane.MicroExcel import MicroExcel
from jane.ImportExcel import ImportExcel
from jane.Template import Template

class JaneP(object):
    
    def __init__(self):
        self.mth=datetime.now().month
        
        
        self.sheetName='interface1'
        
        self.pres=Template()
        # pres.getAllAccounts(template, self.repos)
        self.google_cres="/Users/pengwang/Downloads/JaneProject-614aeb27e1fc.json"
        self.google=False


        
    def doProcess(self):
        if(self.google):
            self.ie=ImportExcel()
        else:
            self.ie=MicroExcel()
        self.ie.loadSheet(self.ie.fileName)
        self.repos=self.ie.repos
        self.template=self.ie.loadTemplate(self.sheetName)
        self.outputData=self.pres.getAllAccounts(self.template, self.repos)
        
        self.ie.writeToSheet( self.outputData, self.template)
        
    def main(self,argv):
        
        #if argv == []:
        #   print("Usage: " + sys.argv[0] + " -h for help")
            #return
        try:
            # opts, args = getopt.getopt(argv,"hf:o:",["ifile=","ofile="])
            opts, args = getopt.getopt(argv, "hg:f:t:o:", ["help","google Drive","file=","template=","output="])
        except getopt.GetoptError:
            print("Usage: " + sys.argv[0] + " -h for help")
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('Syntax: ' + sys.argv[0] + ' \n\n -h help.\n -g google Drive. cres Path and Name \n -f file path and name.\n  -p presentation name.\n -o output path and file name.\n')
                sys.exit()
            elif opt in ("-g", "-google"):
                self.google=True
                self.google_cres=arg
            elif opt in ("-f","-file"):
                self.ie.fileName=arg
            elif opt in ("-t","-template"):
                self.ie.sheetName=arg.lower()
            elif opt in ("-o","-output"):
                self.ie.outputName=arg
            
        self.doProcess()

if __name__ == "__main__":
    jan=JaneP()
    jan.main(sys.argv[1:])


