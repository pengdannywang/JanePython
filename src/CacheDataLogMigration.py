import subprocess
import os.path
import sys, getopt
import calendar
from datetime import datetime
class CacheDataLogMigration():
 
 
    def __init__(self):
        self.mode="stage"
        self.file_path="/tmp/"
        self.filename="cacheDataLog"
        self.u_name = "deploy"
        self.serverID = 'stag02.livngds.com'
        self.targetPath='/BACKUP/database/csv/'
        self.backupPath='/backup/database/csv/'
        self.targetDbServerId='icebox'
        self.firstDay=None
        self.lastDay=None
        self.uploadOnly=False
        self.copyOnly=False
        if(self.mode=="production"):
            self.u_name = "deploy"
            self.serverID = 'central.livngds.com'
    def initialFileNmae(self,year=None,month=None,monthRange=None):
        if (year is None):
            year=datetime.now().year
        if (month is None):
            month=datetime.now().month-1
        self.firstDay,self.lastDay=self.timeRange(year,month,monthRange)
        self.filename=self.filename+"_"+self.firstDay+"_"+self.lastDay+".csv"
         
    def migration(self):
        pathfile=self.file_path+self.filename
         
        where="where logdate>='\\''"+self.firstDay+"'\\'' and logdate <='\\''"+self.lastDay+"'\\''"
        cmdr = "sudo -s su postgres -c \"psql -d livngds_central_journal  -c '\\copy (select * from cachedatalog "+where+") to '\\''"+pathfile+"'\\'''\""
        #print(cmdr)
        try:
            print ("\n=== COPYING data from table CacheDataLog between "+self.firstDay+" and "+self.lastDay+" into :"+pathfile+" on "+self.serverID+" ===\n")
            ssh = subprocess.Popen(["ssh","-p33322",self.u_name+'@'+ self.serverID, cmdr], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result=ssh.stdout.readline()
            print("\n=== "+ result.decode("utf-8").strip("\n")+" records into "+pathfile+"  ===\n")
            cmdr = "sudo -s su postgres -c \"psql -d livngds_central_journal  -c 'delete from cachedatalog "+where+"'\""
            print ("=== DELETING data from table CacheDataLog between "+self.firstDay+" and "+self.lastDay+" ===")
            ssh = subprocess.Popen(["ssh","-p33322",self.u_name+'@'+ self.serverID, cmdr], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result=ssh.stdout.readline()
            print("\n=== "+ result.decode("utf-8").strip("\n")+" records in table CacheDataLog on "+self.serverID+" ===\n")
 
        except ValueError:
            print("an error occurred , error:"+ssh.stderr.readlines())
             
    def copyFileToTargetLocation(self):
        try:
            print("\n=== COPYING :"+self.file_path+self.filename+" to /BACKUP/database/csv/ ......  ===\n")
            print("\n    copying ......  \n\n")
            ssh = subprocess.Popen(["scp","-P33322",self.serverID+":"+self.file_path+self.filename,self.targetPath],shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result=ssh.stdout.readline()
            if(os.path.isfile(self.targetPath+self.filename)):
                print("\n=== COMPLETED copy file ===\n")
            else:
                print("UNSUCCESSFUL copied "+self.filename +" to "+self.targetPath)
        except ValueError:
            print("an error occurred , error:"+result)
             
    def uploadFileToTargetDb(self):
        try:
            existfile=False
            if(os.path.isfile(self.targetPath+self.filename)):
                existfile=True
            if(existfile):
                print("\n=== UPLOADING :"+self.file_path+self.filename+" to "+self.targetDbServerId+"  ===\n")
                print("\n    Uploading ......  \n\n")
                cmdr = "sudo su - postgres -c \"psql -d livngds_central_journal  -c '\copy cachedatalog from  '\\''"+self.backupPath+self.filename+"'\\'' '\""
                 
                ssh = subprocess.Popen(["ssh",self.u_name+'@'+ self.targetDbServerId, cmdr], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result=ssh.stdout.readline()
                print("\n=== "+ result.decode("utf-8").strip("\n")+" records in table CacheDataLog on "+self.targetDbServerId+" ===\n")
            else:
                print(self.targetPath+self.filename+" doesn't exist")
        except ValueError:
            print("an error occurred , error:"+result)
             
    def timeRange(self,year,month,monthRange):
        year=int(year)
        month=int(month)
        firstDay=str(year)+"-"+'{:02}'.format(month)+"-"+"01"
        if(monthRange is not None):
            if(int(monthRange)>=1):
                monthRange=int(monthRange)-1
            monthRange=int(monthRange)
            month=month+monthRange
       
        lastDay=str(year)+"-"+'{:02}'.format(month)+"-"+str(calendar.monthrange(year, month).__getitem__(1))
        return (firstDay,lastDay)
     
    def checkDate(self,year,month):
        correctDate = True
        try:
            datetime(int(year), int(month), 1)
            correctDate = True
        except ValueError:
            correctDate = False
            print("Input "+year +" or "+month+" is not valid, please check")
        return correctDate
     
    def checkMonthRange(self,monthRange):
        correctMonthRange = None
        if(monthRange.isdigit() and int(monthRange)>0 and int(monthRange)<13):
            correctMonthRange = True
        else:
            correctMonthRange = False
            print("Input "+monthRange+" must be only an integer between 1 and 12 , please check")
        return correctMonthRange
     
    def main(self,argv):
        if argv == []:
            print("Usage: " + sys.argv[0] + " -h for help")
            return
        try:
            # opts, args = getopt.getopt(argv,"hf:o:",["ifile=","ofile="])
            opts, args = getopt.getopt(argv, "hm:u:cl", ["help","mode=","user=","copy","upload"])
        except getopt.GetoptError:
            print("Usage: " + sys.argv[0] + " -h for help")
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('Syntax: ' + sys.argv[0] + ' \n\n -h help.\n -m modes stage : stag02.livngdes.com. / product : central.livngds.com.\n -u userName default: deploy.\n -l only run uploading data to icebox database default: false.\n [year month monthRange] default: previous month.\n')
                sys.exit()
            elif opt in ("-m", "-mode"):
                if(arg.lower()=="production"):
                    self.mode="production"
            elif opt in ("-u","-user"):
                self.u_name=arg.lower()
            elif opt in ("-c","-copy"):
                self.copyOnly=True
            elif opt in ("-l","-upload"):
                self.uploadOnly=True
             
        correctArgv=False
        year=None
        month=None
        monthRange=None
        #maxmum of args is 4. 
        if(len(args)<=4) :
            if(len(args)>=3) and (self.checkDate(args[0],args[1])):
                year=args[0]
                month=args[1]
                correctArgv=True
            if (len(args)==3) and (self.checkMonthRange(args[2])): #monthRange is args=3
                monthRange=args[2]
                correctArgv=True
        if(correctArgv) or len(args)==0:
            self.initialFileNmae(year, month, monthRange)
            if(self.copyOnly):
                self.copyFileToTargetLocation()
                sys.exit(2)
            if(self.uploadOnly):
                self.uploadFileToTargetDb()
                sys.exit(2)
            if(os.path.isfile(self.targetPath+self.filename)):
                print("\n=== "+self.filename+" exists in "+self.targetPath+", abort migration===\n")
            else:
                self.migration()
                self.copyFileToTargetLocation()
                self.uploadFileToTargetDb()
                print("\n=== COMPLETED ===\n")
        else:
            print("Wrong inputs. Please check")
if __name__ == "__main__":
    livn=CacheDataLogMigration()
    livn.main(sys.argv[1:])