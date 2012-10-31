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
    lines = f.read().splitlines()
    username = str(lines[0])
    email = str(lines[1])
    f.close()
    return (username,email)

def getHashNameFromHashmap(hashfile,name):
    fp = open(hashfile,'r')
    lines = fp.read().splitlines()
    for line in lines:
        sp = line.split(" ")
        if sp[0] == name:
            return sp[1]
    return None 
        



