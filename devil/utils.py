def fileTracked(filename,tracking_file):
    files=open(tracking_file,'U')
    lines=files.readlines();
    files.close()
    for line in lines:
        path=line.split(" ")
        if(path[0] == os.path.abspath(filename)):
            return False 
    return True 


