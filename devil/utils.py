import os 

def fileTracked(filename,tracking_file):
    files=open(tracking_file,'r')
    lines=files.readlines();
    files.close()
    for line in lines:
        path=line.split(" ")
        if(path[0] == os.path.abspath(filename)):
            return False 
    return True 

def getUsername(ufile):
    f = open(ufile,'r')
    username = str(f.readline())
    email = str(f.readline())
    f.close()
    return (username,email)


