from datetime import timezone
import datetime
import os
# Getting the current date  
# and time

def GetTime():
    dt = datetime.datetime.now()
    utc_time = dt.replace(tzinfo = timezone.utc)
    return(str(utc_time.timestamp()))

LogFolder = os.getcwd()+"\Logs"
Log = ("\Log-"+str(GetTime())+".log")

#Create Log Folder if it doesn't exist
if (os.path.isdir(LogFolder) == False):
    os.mkdir(LogFolder)

def Add(message,author):
    print (message)
    f = open(LogFolder+str(Log), "a")
    f.write('\n'+str(message)+","+str(author)+","+str(GetTime()))
    f.close()
    return

print("Created Log at - "+LogFolder+Log)
