import exceptions,os

class FileController(object):
    """
    Class to perform all the local functionalities of the version
    control system.
    """
    def __init__(self,directory):
        """
        Args:
          directory(str): Full path of the directory where the
          version control is initiated.
        Returns:
          FileController Object
        """
        self.directory = directory
	#self.dictionary = []

    def start(self):
        """
        Initiates the repository
        """
	try:
		os.makedirs(self.directory)
	except OSError, e:
	        if e.errno != errno.EEXIST:
        	    raise
        

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
	if (os.path.isfile(filename) == True):
		#self.dictionary.append((os.path.abspath(filename),'notcommited'))
		files=open('files.txt','U')
		lines=files.readlines();
		files=open('files.txt','w')
		for line in lines:
			path=line.split(" ")
			if(path[0] == os.path.abspath(filename)):
				files.write(path[0] + " " + "notcommited\n")
			else:
				files.write(line)
				
	elif (os.path.isdir(filename) == True):
		for f in os.listdir(filename):
			if (os.path.isfile(f) == True): 
				#self.dictionary.append((os.path.abspath(f),'notcommited'))
				files=open('files.txt','U')
				lines=files.readlines();
				files=open('files.txt','w')
				for line in lines:
					path=line.split(" ")
					if(path[0] == os.path.abspath(filename)):
						files.write(path[0] + " " + "notcommited\n")
					else:
						files.write(line)
			elif (os.path.isdir(f) == True):
				self.add(f)
	else:
		raise FileOrDirectoryDoesNotExist()	


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
        files=open('files.txt','U')
	lines=files.readlines();
	for line in lines:
		path=line.split(" ")
		if (path[1]== "notcommited\n"):
			print line

    def pull(self,url):
        pass

    def push(self,url):
        pass

    def revert(self,commit_hash):
        pass
