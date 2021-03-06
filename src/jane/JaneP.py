'''
Created on 23 Jul. 2018

@author: pengwang
'''

from datetime import datetime

import sys, getopt
from MicroExcel import MicroExcel
from GoogleExcel import GoogleExcel
from Template import Template 
import pandas as pd
class JaneP(object):

    def __init__(self):
        self.mth=datetime.now().month


        self.sheetName='interface1'
        self.path=''
        self.pres=Template()
        # pres.getDataWithTemplateOrder(templateWorkSheet, self.repos)
        #self.google_cres="E:/downloads/JaneProject-f472d80e0028.json"
        self.google_cres="E:/downloads/JaneProject-f472d80e0028.json"
        self.google=False
        self.fileName='entityConfig.xlsx'
        #self.fileName='/Users/pengwang/Downloads/entityConfig.xlsx'
        self.googleFile='entityConfig'
        #self.outputFile='/Users/pengwang/Downloads/output.xlsx'
        self.outputFile='output.xlsx'


    def doProcess(self):
        self.fileName='entityConfig.xlsx'

        if(self.google):
            self.io=GoogleExcel()
            self.io.loadSheet(self.google_cres)
        else:
            self.io=MicroExcel()
            self.io.loadSheet(self.path,self.fileName)
        self.repos=self.io.repos
		
    def createTemplate(self):
        templateDFs=pd.DataFrame(self.io.templates.values) # convert worksheets to dataFrame structure
        for i in range(1,len(templateDFs)): #loop all templates
            path=templateDFs.iloc[i][0]
            if(pd.isnull(path)):
                fileName=self.path+templateDFs.iloc[i][1]
            else:
                fileName=path+templateDFs.iloc[i][1]
            sheet=templateDFs.iloc[i][2]

            #self.writeToSheet(fileName, sheet,outputData, template)
            self.templateWorkSheet=self.io.loadTemplateWorkSheet(sheet)
            self.outputData=self.pres.getDataWithTemplateOrder(self.templateWorkSheet, self.repos)

            self.io.writeToSheet(fileName, sheet,self.outputData, self.templateWorkSheet)



            # self.io.writeToSheet(self.outputFile, self.sheetName,self.outputData, self.templateWorkSheet)



    def main(self,argv):

        #if argv == []:
        #   print("Usage: " + sys.argv[0] + " -h for help")
            #return
        try:
            # opts, args = getopt.getopt(argv,"hf:o:",["ifile=","ofile="])
            opts, args = getopt.getopt(argv, "hgf:t:o:n", ["help","google Drive","file=","templateWorkSheet=","output=","noTemplate"])
        except getopt.GetoptError:
            print("Usage: " + sys.argv[0] + " -h for help")
            #sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('Syntax: ' + sys.argv[0] + ' \n\n -h help.\n -g google Drive. cres Path and Name \n -f file path and name.\n  -p presentation name.\n -o output path and file name.\n')
                sys.exit()
            elif opt in ("-g", "-google"):
                self.google=True
                self.google=True
                #self.google_cres=arg
            elif opt in ("-f","-file"):
                self.path=arg
            elif opt in ("-t","-template"):
                self.sheetName=arg.lower()
            elif opt in ("-o","-output"):
                self.outputName=arg

            if opt in ("-n","-noTemplate"):
                self.doProcess()
            else:
                self.doProcess()
                self.createTemplate()


if __name__ == "__main__":
    jan=JaneP()
    jan.main(sys.argv[1:])


