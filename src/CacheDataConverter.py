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
        self.mode="local"

        self.path = '/root/'
        self.voltdb_path="/opt/voltdb"
        self.snapshot_name = 'AUTOSNAP_2018.11.26.00.25.03'
        self.empty_snapshot_name='emptysnapshot'
        self.empty_snapshot_path='emptysnapshot/'
        self.inputs_name= 'inputs.txt'
        self.voltdb={
            "tables":["CACHEDATA",'OPERATORMETA','PRODUCTMETA'],
            "files":["CACHEDATA.csv",'OPERATORMETA.csv','PRODUCTMETA.csv']
        }
        self.symbal='\n--------------------'
        self.symbal_end='--------------------\n'



    def check_empty_voltdb(self):
        file=Path(self.path+self.empty_snapshot_path+self.empty_snapshot_name+".jar")
        if file.is_file():
            return True
        else:
            print(self.symbal+self.empty_snapshot_name+" isn't exists")
            return False
    def check_product_snapshot(self):
        file=
    def load_empty_voltdb_schema(self):

            if(self.check_empty_voltdb()):
                ssh = subprocess.Popen(["voltadmin", "status"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                if('hostcount') in str(ssh.stdout.read()):
                    print(self.symbal+"voltadmin shutdown"+self.symbal_end)
                    ssh = subprocess.Popen(["voltadmin", "shutdown"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    ssh.wait()
                print(self.symbal+"voltdb init"+self.symbal_end)
                ssh = subprocess.Popen(["voltdb", "init", "--config",self.voltdb_path+"/deployment.xml","--dir" ,self.voltdb_path,"--force"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ssh.wait()
                #ssh = subprocess.Popen(["voltdb", "start", "--pause","--dir" ,self.voltdb_path,"--host","localhost"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                cmd="voltdb start --dir "+self.voltdb_path+" --host localhost --pause &"
                print(self.symbal+cmd)
                os.system(cmd)
                while True:
                    ssh = subprocess.Popen(["voltadmin", "status"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if("ERROR" in str(ssh.stdout.readline())):
                        print(self.symbal+"sleep 2 seconds ")
                        time.sleep(2)
                        pass
                    else:

                        break

                ##os.system("voltdb restore "+self.path+self.empty_snapshot_path+" "+self.empty_snapshot_name)
                print(self.symbal+"voltadmin restore"+self.symbal_end)
                ssh = subprocess.Popen(["voltadmin", "restore","/root/emptysnapshot/","emptysnapshot"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ssh.wait()
                print(ssh.stdout.read())
                ssh = subprocess.Popen(["voltadmin", "resume"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ssh.wait()
                print(ssh.stdout.read())


    def convert_production_to_csv(self):

        print(self.symbal+"snapshotconvert "+self.snapshot_name+self.symbal_end)
        ssh = subprocess.Popen(["snapshotconvert", self.snapshot_name, "--dir", self.path, "--table", self.voltdb['tables'][0], "--table", self.voltdb['tables'][1], "--table", self.voltdb['tables'][2], "--type", "csv", "--outdir", self.path], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ssh.wait()
        print(ssh.stdout.readline())
        print(self.symbal+"done conversion"+self.symbal_end)

    def queryDataset(self):
        print(self.symbal+"read csv files : "+self.voltdb['files'].__str__()+self.symbal_end)
        #load csv files
        cachedata=pd.read_csv(self.path+self.voltdb['files'][0],header=None)
        operatormeta=pd.read_csv(self.path+self.voltdb['files'][1],header=None)
        productmeta=pd.read_csv(self.path+self.voltdb['files'][2],header=None)

        print(self.symbal+"read csv files : " + self.inputs_name +self.symbal_end)
        #contains operatorcid and productcid to be used to filter out data from loaded csv files
        inputs=pd.read_json(self.inputs_name)
        print(self.symbal+"Done loading"+self.symbal_end)

        print("\n-----------------------------------  querying data by operatorcid and productcid  ------------------------------------------\n"+self.symbal_end)
        cachedf=[]
        productmetadf=[]
        operatormetadf=[]

        for row in inputs.iterrows():
            if(len(row[1][1])==0):
                cachedf.append(cachedata[cachedata[0] == row[1][0]])
                productmetadf.append(productmeta[productmeta[0] == row[1][0]])
                operatormetadf.append(operatormeta[operatormeta[0] == row[1][0]])
            else:
                cachedf.append(cachedata[cachedata[1].isin(row[1][1])])
                productmetadf.append(productmeta[productmeta[1].isin(row[1][1])])
                operatormetadf.append(operatormeta[operatormeta[1].isin(row[1][1])])

        #merge data sets to be a dataframe
        cache_result=pd.concat(cachedf)
        productmeta_result=pd.concat(productmetadf)
        operatormeta_result=pd.concat(operatormetadf)

        #save a dataframe to csv files
        cache_result.to_csv(self.path+self.voltdb['files'][0],header=False,index=False)
        operatormeta_result.to_csv(self.path+self.voltdb['files'][1],header=False,index=False)
        productmeta_result.to_csv(self.path+self.voltdb['files'][2],header=False,index=False)
        print("\n-----------------------------------Done querying------------------------------------------\n")

    def loadDataToVoltdb(self):

        print("\n-----------------------------------load data to voltdb------------------------------------------\n")

        ssh=subprocess.Popen(["csvloader",self.voltdb['tables'][0],"-f",self.path+self.voltdb['files'][0]], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ssh.wait()
        print(ssh.stdout.read())
        ssh=subprocess.Popen(["csvloader",self.voltdb['tables'][1],"-f",self.path+self.voltdb['files'][1]], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ssh.wait()
        print(ssh.stdout.read())
        ssh=subprocess.Popen(["csvloader",self.voltdb['tables'][2],"-f",self.path+self.voltdb['files'][2]], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ssh.wait()
        print(ssh.stdout.read())
        print("\n-----------------------------------Done loading data to Voltdb------------------------------------------\n")


    def main(self,argv):
        try:
            # opts, args = getopt.getopt(argv,"hf:o:",["ifile=","ofile="])
            opts, args = getopt.getopt(argv, "h:p:s:vp:i", ["help","path","file=","templateWorkSheet=","output=","noTemplate"])
        except getopt.GetoptError:
            print("Usage: " + sys.argv[0] + " -h for help")
            #sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('Syntax: ' + sys.argv[0] + ' \n\n -h help.\n -g google Drive. cres Path and Name \n -f file path and name.\n  -p presentation name.\n -o output path and file name.\n')
                sys.exit()
            elif opt in ("-p","--path"):
                self.path="/"+arg+"/"
            elif opt in ("-s", "--snapshot"):
                self.snapshot_name=arg.upper()
            elif opt in ("-vp","--voltdb_path"):
                self.voltdb_path=arg.lower()
            elif opt in ("-i","-input"):
                self.inputs_name=arg.lower()
        print("path=="+self.path)
        if not self.check_empty_voltdb():
            exit(0)

        self.load_empty_voltdb_schema()
        self.convert_production_to_csv()
        self.queryDataset()
        self.loadDataToVoltdb()
if __name__ == "__main__":
    cd=Cachedata()
    cd.__init__()
    cd.main(sys.argv[1:])

