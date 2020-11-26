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
	return(str(utc_time.timestamp()))
LogFolder = Path(Path().absolute(),"Logs")
Log = LogFolder / ("Log-"+str(GetTime())+".log")

#Create Log Folder if it doesn't exist
LogFolder = Path(Path().absolute(),"Logs")
if (os.path.isdir(LogFolder) == False):
	os.mkdir(LogFolder)

def Add(message,author):
	f = open(Log, "a")
	f.write('\n'+message+","+author+","+str(GetTime()))
	f.close()
	return

print ("Log will be saved at - "+str(Log))