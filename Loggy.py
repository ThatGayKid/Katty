from datetime import timezone
import datetime
import os
import pathlib
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()
# Getting the current date  
# and time

def GetTime():
    dt = datetime.datetime.now()
    utc_time = dt.replace(tzinfo = timezone.utc)
    return(int(utc_time.timestamp()))

LogFolder = Path(Path().absolute(),"Logs")
Logging = os.getenv("LOGGING")

#Create Log Folder if it doesn't exist
if Logging == "1":
    def Create(Name):
        global Log
        global Baseline
        Log = Path(Path().absolute(),"Logs",(Name+" - "+str(GetTime())+".csv"))
        Baseline = GetTime()

        if (os.path.isdir(LogFolder) == False):
            os.mkdir(LogFolder)
        
        f = open(Log,"a")
        f.write("Type,Message,User,TimeStamp\n")
        f.close
    
        print ("Logging Enabled - Log will be saved at - "+str(Log))

    def Add(Message,ctx):
        try:
            Author = str(ctx.author)
        except:
            Author = str(ctx)
            
        print(Message)
        f = open(Log,"a")
        f.write(Message+',"'+Author+'","'+str((GetTime()-Baseline))+'"\n')
        f.close
        
elif Logging == "0":
    def Create(Name):
        print ("Logging Disabled - No Log will be saved")
    def Add(Message,ctx):
        print(Message)
        