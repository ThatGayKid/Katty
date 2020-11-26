from datetime import timezone
import datetime
import os
import pathlib
from pathlib import Path
# Getting the current date  
# and time

def GetTime():
    dt = datetime.datetime.now()
    utc_time = dt.replace(tzinfo = timezone.utc)
    return(int(utc_time.timestamp()))

LogFolder = Path(Path().absolute(),"Logs")
Log = ""

#Create Log Folder if it doesn't exist
def Create(Name):
    global Log
    Log = Path(Path().absolute(),"Logs",(Name+" - "+str(GetTime())+".csv"))
    
    if (os.path.isdir(LogFolder) == False):
        os.mkdir(LogFolder)
        
    f = open(Log,"a")
    f.write("Type,Message,User,TimeStamp\n")
    f.close
    
    print ("Log will be saved at - "+str(Log))

def Add(message,author):
    f = open(Log,"a")
    f.write(str(message)+","+str(author)+","+str(datetime.datetime.utcnow())+'\n')
    f.close
    return