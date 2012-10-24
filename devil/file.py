#! /usr/bin/python
import exceptions,os,shutil,hashlib,datetime
from optparse import OptionParser

class FileController(object):
    """
    Class to perform all the local functionalities of the version
    control system.
    """
    def __init__(self):
        """
        Args:
          directory(str): Full path of the directory where the
          version control is initiated.
        Returns:
          FileController Object
        """
        self.directory = os.getcwd()
	#self.username=''
	#self.dictionary = []
	
    def start(self):
        """
        Initiates the repository
        """
	try:
		os.makedirs(self.directory + '/Devil')
	except OSError, e:
	        if e.errno != errno.EEXIST:
        	    raise
	username=raw_input("Enter username:\n")
	uname=open(self.directory + '/Devil/'+'username.txt','w')
	uname.write(username)
	uname.close()
	files=open(self.directory + '/Devil/'+'files.txt','w')
	files.close()

    def add(self,filename):
        """
        Adds the given file or directory (all files and directories in
        it) to the tracking system. You need to commit before the
        files added are actually tracked.

        Args:
          filename(str) : file or directory name to add
        Raises:
          FileOrDirectoryDoesNotExist : When the file or directory
          does not exist.
        """
	if (os.path.isfile(filename) == True or os.path.isdir(filename) == True):
		#self.dictionary.append((os.path.abspath(filename),'notcommited'))
		files=open(os.path.abspath('Devil/files.txt'),'U')
		lines=files.readlines();
		present=0
		for line in lines:
			path=line.split(" ")
			if(path[0] == os.path.abspath(filename)):
				present=1
		if(present==0):
			print "absent"
			files=open(os.path.abspath('Devil/files.txt'),'w')
			for line in lines:
				files.write(line)
			files.write(os.path.abspath(filename) + " " + "notcommited\n")
			
		elif(present==1):
			files=open(os.path.abspath('Devil/files.txt'),'w')
			for line in lines:
				path=line.split(" ")
				if(path[0] == os.path.abspath(filename)):
					files.write(path[0] + " " + "notcommited\n")
				else:
					files.write(line)
    """				
	elif (os.path.isdir(filename) == True):
		for f in os.listdir(filename):
			if (os.path.isfile(f) == True): 
				#self.dictionary.append((os.path.abspath(f),'notcommited'))
				files=open(os.path.abspath('Devil/files.txt'),'U')
				lines=files.readlines();
				present=0
				for line in lines:
					path=line.split(" ")
					if(path[0] == os.path.abspath(filename + '/' + f)):
						present=1
				if(present==0):
					print "first time"
					files=open(os.path.abspath('Devil/files.txt'),'w')
					for line in lines:
						files.write(line)
					files.write(os.path.abspath(filename + '/' + f) + " " + "notcommited\n")
			
				elif(present==1):
					print "not first time"
					files=open(os.path.abspath('Devil/files.txt'),'w')
					for line in lines:
						path=line.split(" ")
						if(path[0] == os.path.abspath(filename + '/' + f)):
							files.write(path[0] + " " + "notcommited\n")
						else:
							files.write(line)
			elif (os.path.isdir(filename + '/' + f) == True):
				print "adding subdirectory"
				self.add(filename + '/' + f)

	else:
		x=0#raise FileOrDirectoryDoesNotExist()	
    """

    def commit(self,message):
	#hashmap='lkfdsadf'
	uname=open(self.directory + '/Devil/'+'username.txt','U')
	username=str(uname.readlines())
	uname.close()
	dateandtime=str(datetime.datetime.now())
	hashmap=hashlib.sha224(username + dateandtime).hexdigest()
	files=open(os.path.abspath('Devil/files.txt'),'U')
	lines=files.readlines();
	#os.makedirs(os.path.abspath('Devil')+'/object'+'/'+hashmap)
	for line in lines:
		path=line.split(" ")
		if(path[1]=="notcommited\n"):
			if(os.path.isfile(path[0])== True):
				if not (os.path.exists(os.path.abspath('Devil')+'/object'+'/'+hashmap)):
					os.makedirs(os.path.abspath('Devil')+'/object'+'/'+hashmap)
				shutil.copy2(path[0],os.path.abspath('Devil')+'/object'+'/'+hashmap)
			elif(os.path.isdir(path[0])== True):
				shutil.copytree(path[0],os.path.abspath('Devil')+'/object'+'/'+hashmap)
	mfile=open(os.path.abspath('Devil')+'/object'+'/'+hashmap+'/'+'message.txt','w')
	mfile.write(message)
	mfile.close()
	files=open(os.path.abspath('Devil/files.txt'),'w')
	for line in lines:
		path=line.split(" ")
		files.write(path[0] + " commited\n")
	files.close()

    def rename(self,newname):
	if os.path.exists(newname):
		raise DirectoryExist
	else:
		try:
            		os.rename(self.directory, newname)
        	except OSError, e:
            		raise
		

    def clone(self,target):
        pass

    def log(self):
        pass

    def diff(self):
        pass

    def status(self):
        files=open(os.path.abspath('Devil/files.txt'),'U')
	lines=files.readlines();
	for line in lines:
		path=line.split(" ")
		if (path[1]== "notcommited\n"):
			print "File	",path[0],"	",path[1]

    def pull(self,url):
        pass

    def push(self,url):
        pass

    def revert(self,commit_hash):
        pass

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--init", help = "Initialize the repo", dest="init",action= "store_true")
    parser.add_option("-a", "--add", help = "add files to tracking system", dest="add",action= "store")
    parser.add_option("-c", "--commit",help="commit the required changes", dest="commit",action= "store")
    parser.add_option("-s", "--status",help="all not commited files", dest="status",action= "store_true")
    parser.add_option("-l", "--log",help="complete list of commits", dest="log",action= "store_true")
    (options, args) = parser.parse_args()
    if options.init:
        #print("Initializing repo")
	obj=FileController()
	obj.start()
    elif options.add:
	obj=FileController()
	#print options.add
	obj.add(options.add)
    elif options.commit:
	obj=FileController()
	obj.commit(options.commit)
    elif options.status:
	obj=FileController()
	obj.status()
    elif options.log:
	obj=FileController()
        obj.log()


if __name__ == "__main__":
    main()
