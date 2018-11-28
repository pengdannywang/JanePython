import pandas as pd
import subprocess
from pathlib import Path
import sys, getopt
import os
import os.path
import datetime, time
import urllib
class Cachedata(object):
    def __init__(self):
        self.mode="debug"
        self.snapshot_name = 'AUTOSNAP_2018.11.26.00.25.03'
        self.product_snapshot_path = 'C:/tools/'
        self.voltdb={
            "tables":["CACHEDATA",'OPERATORMETA','PRODUCTMETA'],
            "files":["CACHEDATA.csv",'OPERATORMETA.csv','PRODUCTMETA.csv']
        }
        self.empty_snapshot_path='~/db/emptysnapshot'
        self.empty_snapshot_name='emptysnapshot'
        self.voltdb_path="/opt/voltdb/"
        self.output_path = 'e:/tools/'
        u_name = 'root'
        serverID = '10.10.0.18'

        if(mode=="production"):
            snapshot_name = 'AUTOSNAP_2018.11.26.00.25.03'
            input_path = '/root/db/voltdb/'

            u_name = 'root'
            serverID = '10.10.0.18'
    def load_empty_voltdb_schema(self):
        ssh=subprocess.Popen(["voltdb", "start", "--pause","--dir" ,self.voltdb_path], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ssh = subprocess.Popen(["voltadmin", "restore",self.empty_snapshot_path,self.empty_snapshot_name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ssh = subprocess.Popen(["voltadmin", "resume"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def convert_production_by_op_pcid(self,product_snapshot):
        my_file=self.output_path+self.voltdb["tables"][0]
        if (my_file.exists() != True):
            print("no file: ")
        else:
            print("file exists")
            # os.remove(my_file)
        ssh = subprocess.Popen(["/opt/voltdb/bin/snapshotconvert", product_snapshot, "--dir", self.product_snapshot_path, "--table", self.voltdb['tables'][0],"--table", self.voltdb['tables'][1],"--table", self.voltdb['tables'][2], "--type", "csv","--outdir", self.output_path ], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
        ssh.wait()
        cachedata=pd.read_csv(self.output_path+self.voltdb['files'][0],header=None)
        operatormeta=pd.read_csv(self.output_path+self.voltdb['files'][1],header=None)
        productmeta=pd.read_csv(self.output_path+self.voltdb['files'][2],header=None)
        inputs=pd.read_json('c:/tools/inputs.txt')


        cachedf=[]
        productmetadf=[]
        operatormeta=[]
for row in inputs.iterrows():

    if(len(row[1][1])==0):
        cachedf.append(cachedata[cachedata[0] == row[1][0]])
        productmetadf.append(productmeta[productmeta[0] == row[1][0]])
        operatormeta.append(operatormeta[operatormeta[0] == row[1][0]])
    else:
        cachedf.append(cachedata[cachedata[1].isin(row[1][1])])
        productmetadf.append(productmeta[productmeta[1] == row[1][1]])
        operatormeta.append(operatormeta[operatormeta[1] == row[1][1]])

cache_result=pd.concat(cachedf)
cache_result.to_csv(output_path+cache_result_csv,header=False,index=False)
subprocess.Popen(["csvloader","cachedata","-f",output_path+"result.csv"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
productmeta_result=pd.concat(productmetadf)
productmeta_result.to_csv(output_path+"result.csv",header=False,index=False)
subprocess.Popen(["csvloader","cachedata","-f",output_path+"result.csv"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
cache_result=pd.concat(cachedf)
cache_result.to_csv(output_path+"result.csv",header=False,index=False)
subprocess.Popen(["csvloader","cachedata","-f",output_path+"result.csv"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()

