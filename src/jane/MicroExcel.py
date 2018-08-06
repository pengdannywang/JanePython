
'''
Created on 24Jul.,2018

@author: pwang
'''
from oauth2client.service_account import ServiceAccountCredentials
import openpyxl
from openpyxl.styles import Font, Fill
from openpyxl.utils.dataframe import dataframe_to_rows 
import jane.NormalizeRawData as nrd
from jane.NormalizeRawData import COLINDEX as ci
import pandas as pd
import numpy as np
import os
from jane.Template import Template

class MicroExcel(object):

    def __init__(self):
        self.CONFIG_SHEET_ENTITIES = "entities"
        self.CONFIG_SHEET_ACCOUNTS = "accounts"
        self.CONFIG_SHEET_TEMPLATES='templates'
        self.sheetName="interface1"
        self.CONFIG_ENTITIES_FILENAME = 'fileName'
        self.CONFIG_ENTITIES_BUDGET = 'BUDGET'
        self.CONFIG_ENTITIES_ACTUAL = 'ACTUAL'
        self.CONFIG_ENTITIES_PRIOR = 'PRIOR'
        self.budgetDf=pd.DataFrame()
        self.actualDf=pd.DataFrame()
        self.priorDf=pd.DataFrame()

        self.template=Template()

        
    def loadSheet(self,fileName):
        
        self.wb=openpyxl.load_workbook(fileName)
        self.entities=self.wb[self.CONFIG_SHEET_ENTITIES]
        config_cells=self.entities.__getitem__("A3:F200")
        accountSheet=self.wb[self.CONFIG_SHEET_ACCOUNTS]
        self.templates=self.wb[self.CONFIG_SHEET_TEMPLATES]
        config_account_cells=accountSheet.__getitem__("A2:A200")
        self.accountList=nrd.leanupExcelAccountTupleCells(config_account_cells)
        for i in range(len(config_cells)):
            
            file=config_cells[i][0].value
            if pd.isnull(file)==True:
                break
                
            if(pd.isnull(file)!=True):
                priorN=config_cells[i][1].value
                budgetN=config_cells[i][2].value
                actualN=config_cells[i][3].value
                b19N=config_cells[i][4].value
                sheetRange=config_cells[i][5].value
                wb2=openpyxl.load_workbook(file)
                if(budgetN!=''):
                    budgetSheets=wb2[budgetN]
    
                    cells=budgetSheets.__getitem__(sheetRange)
                    budgetDf=nrd.normalizeExcel(ci.INDEX_F18,cells)
                    #budgetDf=nrd.reduceRepositoryByAccounts(budgetDf, self.accountList)
                    if(not self.budgetDf.empty):
                        self.budgetDf=self.budgetDf+budgetDf
                    else:
                        self.budgetDf=budgetDf
    
                if(actualN!=''):   
                    actualSheet=wb2[actualN]
                   
                    cells=actualSheet.__getitem__(sheetRange)
                    actualDf=nrd.normalizeExcel(ci.INDEX_B18,cells)
                    #actualDf=nrd.reduceRepositoryByAccounts(actualDf, self.accountList)
                    if(not self.actualDf.empty):
                        self.actualDf=self.actualDf+actualDf
                    else:
                        self.actualDf=actualDf
                
                if(priorN!=''):
                    priorSheet=wb2[priorN]
                    cells=priorSheet.__getitem__(sheetRange)
                    priorDf=nrd.normalizeExcel(ci.INDEX_A17,cells)
                    #priorDf=nrd.reduceRepositoryByAccounts(priorDf, self.accountList)
                    if(not self.priorDf.empty):
                        self.priorDf=self.priorDf+priorDf
                    else:
                        self.priorDf=priorDf
               
                if(pd.isnull(b19N)!=True):
                    b19sheet=wb2[b19N]
                    cells=b19sheet.__getitem__(sheetRange)
                    b19Df=nrd.normalizeExcel(ci.INDEX_B19,cells)
                    
        self.budgetDf=nrd.reduceRepositoryByAccounts(self.budgetDf, self.accountList)
        self.actualDf=nrd.reduceRepositoryByAccounts(self.actualDf, self.accountList)
        self.priorDf=nrd.reduceRepositoryByAccounts(self.priorDf, self.accountList)
        #b19 is from different files. if it is empty, then set it to zero 
        if(pd.isnull(b19N)!=True):
            self.b19=nrd.reduceRepositoryByAccounts(b19Df, self.accountList)
        else:
            self.b19=nrd.generateB19(self.budgetDf)
        self.repos= self.generateRepos()                       

            
    
    
    def loadTemplate(self,sheetName):
        presentSheets =self.wb[sheetName]
        pCells=presentSheets.__getitem__("A2:F150")
        df=pd.DataFrame(columns=ci.CONFIG_COLUMNS)
        for i in range(0,len(pCells)):
            if(pd.isnull(pCells[i][0].value)!=True):
                row=[pCells[i][0].value,pCells[i][1].value,pCells[i][2].value,pCells[i][3].value,pCells[i][4].value,pCells[i][5].value]
                df.loc[len(df)]=row
        return df
    
    

    
    def generateRepos(self):
        repos=pd.DataFrame()
        repos=repos.append(self.priorDf)
        repos=repos.append(self.actualDf)
        repos=repos.append(self.budgetDf)
        repos=repos.append(self.b19)
        # ensure repos don't have nan value in order to exception 
        repos=repos.replace(np.NaN,0)
        repos=repos.append(nrd.generatef18a17(repos))
        repos=repos.append(nrd.generatef18b18(repos))
        repos=repos.append(nrd.generateb19f18(repos))
        return repos
    
        
    def getSheet(self,outputFile):
        if(os.path.isfile(outputFile)):
            self.workbook=openpyxl.load_workbook(outputFile) #load old booksheet
        else:
            self.workbook=openpyxl.Workbook()#create new workbook
            
    def printTemplates(self,outputData,template):
        templateDFs=pd.DataFrame(self.templates.values) # convert worksheets to dataFrame structure
        for i in range(1,len(templateDFs)): #loop all templates
            path=templateDFs.iloc[i][0]
            fileName=path+templateDFs.iloc[i][1]
            sheet=templateDFs.iloc[i][2]
            
            self.writeToSheet(fileName, sheet,outputData, template)
                       
    def writeToSheet(self,outputFile,sheetName,outputData,template):
        self.getSheet(outputFile)
        sheet=self.workbook.create_sheet(title=sheetName)
        
        #print head months
        row=1
        col=1
        sheet.cell(row,col,ci.INDEX_NAME)
        col=col+1
        for mon in ci.COLUMNS_WITHOUT_INDEXES:
            
            end_col=col+6
            sheet.merge_cells(start_row=row, start_column=col, end_row=row, end_column=end_col)
            sheet.cell(1,col,mon)
            col=end_col+1
           
        # print sub Head as A17,B18...
        row=2
        col=1
        for column in outputData.columns.tolist():
            sheet.cell(row,col,column)
            col=col+1
        # a blank line 
        # print data
        row=4
        for t in template.iterrows():

            d=outputData.query(ci.INDEX_NAME+"=='"+t[1][ci.CONFIG_ACCOUNT]+"'")
            if(~d.empty and len(d)>0):
                # template row is not percentages of other row
                sheet.cell(row,1,d.iloc[0][0])
                for j in range(1,len(d.columns)):
                    col=j+1
                    if(d.columns[j] in ci.INDEX_PERCENTAGES):
                        sheet.cell(row,col,"{:1.0%}".format(d.iloc[0][j]))
                    else:
                        sheet.cell(row,col,"{:,.0f}".format(d.iloc[0][j]))
            else:
                
                if(t[1][ci.CONFIG_LEVEL]==10):
                    percent=self.template.getPercentages(t[1][ci.CONFIG_ACCOUNT], t[1][ci.CONFIG_PRECENTAGES], t[1][ci.CONFIG_DENOMINATOR], outputData)
                    sheet.cell(row,1,percent.iloc[0][0])
                    for j in range(1,len(percent.columns)):
                        col=j+1
                        #format to %

                        sheet.cell(row,col,"{:1.0%}".format(percent.iloc[0][j]))
                        
                else:
                    sheet.cell(row,1,t[1][ci.CONFIG_ACCOUNT])
#             if(t[1][ci.CONFIG_LEVEL!='1']):
#                 rowA=sheet.row_dimensions[row]
#                 rowA.font=Font(b="border")
            row=row+1 

        #self.wb.save(self.fileName)

        self.workbook.save(outputFile)
if __name__ == "__main__":
    ie=MicroExcel()
    ie.loadSheet(ie.fileName)
    print(ie.repos)
    



