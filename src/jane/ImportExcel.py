
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

class ImportExcel(object):

    def __init__(self):
        self.budgetDf=pd.DataFrame()
        self.actualDf=pd.DataFrame()
        self.priorDf=pd.DataFrame()
        # use creds to create row client to interact with the Google Drive API
        scope =  ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name("C:/tools/JaneProject-f472d80e0028.json", scope)
        self.client = gspread.authorize(creds)    
        # Find row workbook by name and open the first sheet
        # Make sure you use the right name here.
        #sheet = client.open_by_key("AIzaSyBa1wrSY683ni4DHIuxNSJaLhuuxJA5XCI").sheet1
        self.co=self.client.open("entityConfig")
        self.config1 = self.co.worksheet("entities").get_all_records(head=2)
        self.accountList=self.co.worksheet("accounts").get_all_values()
        self.accountList=nrd.removeEmptyRowForAccountList(self.accountList)
        #sheet =gspread.Worksheet("entityConfig")
        #gspread.Client.open_by_key("AIzaSyBa1wrSY683ni4DHIuxNSJaLhuuxJA5XCI")
        # Extract and print all of the values
        


        
    def loadFiles(self):
        for file in self.config1:
            
            #js=json.loads(str(file).strip('{}').replace("'", "\""))
            fileName=file.get('fileName')
            budgetN=file.get('BUDGET')
            actualN=file.get('ACTUAL')
            priorN=file.get('PRIOR')
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
            self.generateRepos()

    
    def loadPresentation(self,sheetName):
        presentListlists = self.co.worksheet(sheetName).get_all_values()
        df=pd.DataFrame(columns=ci.CONFIG_COLUMNS)
        for i in range(1,len(presentListlists)):
            row=[presentListlists[i][0],presentListlists[i][1],presentListlists[i][2],presentListlists[i][3],presentListlists[i][4]]
            df.loc[len(df)]=row
        return df
    
    
    def getSubByArray(self,names):
        return self.repos.query("name in "+str(names))
    
    
    def generateRepos(self):
        self.repos=pd.DataFrame()
        self.repos=self.repos.append(self.priorDf)
        self.repos=self.repos.append(self.actualDf)
        self.repos=self.repos.append(self.budgetDf)
        self.repos=self.repos.append(self.b19)
        # ensure repos don't have nan value in order to exception 
        self.repos=self.repos.replace(np.NaN,0)
        self.repos=self.repos.append(nrd.generatef18a17(self.repos))
        self.repos=self.repos.append(nrd.generatef18b18(self.repos))
        self.repos=self.repos.append(nrd.generateb19f18(self.repos))
    
       
if __name__ == "__main__":
    ie=ImportExcel()
    ie.loadFiles()
    print(ie.repos)

