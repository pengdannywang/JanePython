
'''
Created on 24Jul.,2018

@author: pwang
'''
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import jane.NormalizeRawData as nrd
from jane.NormalizeRawData import COLINDEX as ci
import pandas as pd
import numpy as np

class GoogleExcel(object):

    def __init__(self):
        self.budgetDf=pd.DataFrame()
        self.actualDf=pd.DataFrame()
        self.priorDf=pd.DataFrame()
        self.fileName='entityConfig'
        self.CONFIG_SHEET_ENTITIES = "entities"
        self.CONFIG_SHEET_ACCOUNTS = "accounts"
        self.CONFIG_SHEET_TEMPLATES='templates'
        self.sheetName="interface1"
        self.CONFIG_ENTITIES_FILENAME = 'fileName'
        self.CONFIG_ENTITIES_BUDGET = 'BUDGET'
        self.CONFIG_ENTITIES_ACTUAL = 'ACTUAL'
        self.CONFIG_ENTITIES_PRIOR = 'PRIOR'
        
    def loadSheet(self,scedsFile):

        # use creds to create row client to interact with the Google Drive API
        scope =  ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(scedsFile, scope)
        self.client = gspread.authorize(creds)    
        # Find row workbook by name and open the first sheet
        # Make sure you use the right name here.
        #sheet = client.open_by_key("AIzaSyBa1wrSY683ni4DHIuxNSJaLhuuxJA5XCI").sheet1
        self.co=self.client.open(self.fileName)
        
        self.config1 = self.co.worksheet(self.CONFIG_SHEET_ENTITIES).get_all_records(head=2)
        self.templates=self.co.worksheet(self.CONFIG_SHEET_TEMPLATES).get_all_values()
        self.accountList=self.co.worksheet(self.CONFIG_SHEET_ACCOUNTS).get_all_values()
        self.accountList=nrd.removeEmptyRowForAccountList(self.accountList)
        
        #sheet =gspread.Worksheet("entityConfig")
        #gspread.Client.open_by_key("AIzaSyBa1wrSY683ni4DHIuxNSJaLhuuxJA5XCI")
        # Extract and print all of the values
        self.repos=self.getRepos()
        
    def getRepos(self):
        for file in self.config1:
            
            #js=json.loads(str(file).strip('{}').replace("'", "\""))
            
            fileName=file.get(self.CONFIG_ENTITIES_FILENAME )
            
            budgetN=file.get(self.CONFIG_ENTITIES_BUDGET)
            
            actualN=file.get(self.CONFIG_ENTITIES_ACTUAL)
           
            priorN=file.get(self.CONFIG_ENTITIES_PRIOR)
            co = self.client.open(fileName)
            if(budgetN!=''):
                rawBudget=co.worksheet(budgetN).get_all_values()
                budgetDf=nrd.normalize(ci.INDEX_F18,rawBudget)
                #budgetDf=nrd.reduceRepositoryByAccounts(budgetDf, self.accountList)
                if(not self.budgetDf.empty):
                    self.budgetDf=self.budgetDf+budgetDf
                else:
                    self.budgetDf=budgetDf

            if(actualN!=''):   
                rawActual=co.worksheet(actualN).get_all_values()
                actualDf=nrd.normalize(ci.INDEX_B18,rawActual)
                #actualDf=nrd.reduceRepositoryByAccounts(actualDf, self.accountList)
                if(not self.actualDf.empty):
                    self.actualDf=self.actualDf+actualDf
                else:
                    self.actualDf=actualDf
            
            if(priorN!=''):
                rawPrior=co.worksheet(priorN).get_all_values()
                priorDf=nrd.normalize(ci.INDEX_A17,rawPrior)
                #priorDf=nrd.reduceRepositoryByAccounts(priorDf, self.accountList)
                if(not self.priorDf.empty):
                    self.priorDf=self.priorDf+priorDf
                else:
                    self.priorDf=priorDf

            self.budgetDf=nrd.reduceRepositoryByAccounts(self.budgetDf, self.accountList)
            self.actualDf=nrd.reduceRepositoryByAccounts(self.actualDf, self.accountList)
            self.priorDf=nrd.reduceRepositoryByAccounts(self.priorDf, self.accountList)
            self.b19=nrd.generateB19(self.budgetDf)
            return self.generateRepos()

    
    def loadTemplateWorkSheet(self,sheetName):
        presentListlists = self.co.worksheet(sheetName).get_all_values()
        df=pd.DataFrame(columns=ci.CONFIG_COLUMNS)
        for i in range(1,len(presentListlists)):
            row=[presentListlists[i][0],presentListlists[i][1],presentListlists[i][2],presentListlists[i][3],presentListlists[i][4],presentListlists[i][5]]
            df.loc[len(df)]=row
        return df
    
    
    def getSubByArray(self,names):
        return self.repos.query("name in "+str(names))
    
    
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
        name="output_"+sheetName
        sheets=self.co.worksheets()
        for sheet in sheets:
            if sheet.title==name :
               
                return sheet
        
                
        return self.co.add_worksheet(name,200,200)
    
    def writeToSheet(self,fName,sheetName,outputData,templateWorkSheet):

        sheet=self.getSheet(sheetName)
        sheet.clear()
        row=1
        col=5
        for mon in ci.COLUMNS_WITHOUT_INDEXES:
            sheet.update_cell(row, col, mon)
            col=col+7

        sheet.insert_row(outputData.columns.tolist(),2)
        
        row=4
        for i in range(len(templateWorkSheet)):

            d=outputData.query(ci.INDEX_NAME+"=='"+templateWorkSheet.iloc[i][1]+"'")
            if(~d.empty and len(d)>0):
                sheet.insert_row(d.iloc[0].tolist(),row)
            else:
                sheet.insert_row(templateWorkSheet.iloc[i][1],row)
            row=row+1
 
    def printTemplates(self,outputData,template):
        for i in range(1,len(self.templates)):
            path=self.templates[i][0]
            fileName=path+self.templates[i][1]
            sheet=self.templates[i][2]
           
            self.writeToSheet(fileName, sheet,outputData, template)  
      

if __name__ == "__main__":
    ie=GoogleExcel()
    ie.loadSheet(ie.fileName)


