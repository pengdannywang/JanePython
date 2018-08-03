
'''
Created on 24Jul.,2018

@author: pwang
'''
from oauth2client.service_account import ServiceAccountCredentials
import openpyxl
import jane.NormalizeRawData as nrd
from jane.NormalizeRawData import COLINDEX as ci
import pandas as pd
import numpy as np

class MicroExcel(object):

    def __init__(self):
        self.budgetDf=pd.DataFrame()
        self.actualDf=pd.DataFrame()
        self.priorDf=pd.DataFrame()
        self.fileName='U:/tools/jane/entityConfig.xlsx'
        

        
    def loadSheet(self,fileName):
        self.fileName=fileName
        self.wb=openpyxl.load_workbook(fileName)
        self.entities=self.wb["entities"]
        config_cells=self.entities.__getitem__("A3:F100")
        accountSheet=self.wb["accounts"]
        config_account_cells=accountSheet.__getitem__("A2:A160")
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
                if(b19N!=''):
                    b19sheet=wb2[b19N]
                    cells=b19sheet.__getitem__(sheetRange)
                    b19Df=nrd.normalizeExcel(ci.INDEX_B19,cells)
                    
        self.budgetDf=nrd.reduceRepositoryByAccounts(self.budgetDf, self.accountList)
        self.actualDf=nrd.reduceRepositoryByAccounts(self.actualDf, self.accountList)
        self.priorDf=nrd.reduceRepositoryByAccounts(self.priorDf, self.accountList)
        #b19 is from different files. if it is empty, then set it to zero 
        if(pd.isnull(b19Df)!=True):
            self.b19=nrd.reduceRepositoryByAccounts(b19Df, self.accountList)
        else:
            self.b19=nrd.generateB19(self.budgetDf)
        self.repos= self.generateRepos()                       

            
    
    
    def loadTemplate(self,sheetName):
        presentSheets =self.wb[sheetName]
        pCells=presentSheets.__getitem__("A2:F150")
        df=pd.DataFrame(columns=ci.CONFIG_COLUMNS)
        for i in range(1,len(pCells)):
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
    
    def getSheet(self,sheetName):
        sheetNames=self.wb.get_sheet_names()
        if(sheetNames.__contains__(sheetName)):
            
            sheet=self.wb[sheetName]
            self.wb.remove(sheet)
           
        sheet=self.wb.create_sheet(title=sheetName)
        return sheet
    
    def writeToSheet(self,sheetName,outputData,template):
        accounts=template[ci.CONFIG_ACCOUNT]
        sheet=self.getSheet(sheetName)
        row=1
        col=1
        sheet.cell(row,col,ci.INDEX_NAME)
        col=col+4
        for mon in ci.COLUMNS_WITHOUT_INDEXES:
            sheet.cell(1,col,mon)
            sheet
            col=col+7
        row=2
        col=1
        for column in outputData.columns.tolist():
            sheet.cell(row,col,column)
            col=col+1
        row=4
        for acc in accounts:
            d=outputData.query(ci.INDEX_NAME+"=='"+acc+"'")
            if(~d.empty and len(d)>0):
                for j in range(0,len(d.columns)):
                    col=j+1
                    sheet.cell(row,col,d.iloc[0][j])
            else:
                sheet.cell(row,1,acc)
            row=row+1 

        self.wb.save(self.fileName)
        
if __name__ == "__main__":
    ie=MicroExcel()
    ie.loadSheet(ie.fileName)
    print(ie.repos)
    



