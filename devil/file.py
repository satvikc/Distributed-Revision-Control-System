#! /usr/bin/python
import exceptions,os,shutil,hashlib,datetime,filecmp
from optparse import OptionParser
from utils import fileTracked,getUsername

	
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
	self.statusfile = os.path.abspath(os.path.join(self.directory,'Devil','status.txt'))
	self.userfile=os.path.abspath(os.path.join(self.directory,'Devil','username.txt'))
	self.trackingfile=os.path.abspath(os.path.join(self.directory,'Devil','files.txt'))
        self.objectdir = os.path.abspath(os.path.join(self.directory,'Devil','object'))

    def start(self):
        """
        Initiates the repository
        """

        try:
                os.makedirs(self.directory + '/Devil')
        except OSError(e):
                if e.errno != errno.EEXIST:
                    raise
        username = input("Enter username:\n")
        email = input("Enter email \n")
        uname=open(self.userfile,'w')
        uname.write(username+'\n')
        uname.write(email+'\n')
        uname.close()
        files=open(self.directory + '/Devil/'+'files.txt','w')
        files.close()
	files=open(self.directory + '/Devil/'+'status.txt','w')
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
        filename = os.path.abspath(filename)
        if(os.path.isdir(filename)):
            for i in os.listdir(filename):
                self.add(i)
        else:
            if(fileTracked(filename,self.trackingfile)):
                print(filename + " => File added to tracking")
                files=open(self.trackingfile,'a')
                files.write(filename + " => notcommited\n")
                files.close()
            else:
                print(filename + " => File already tracked")

    def commit(self,message):
        username,email = getUsername(self.userfile)
        dateandtime=str(datetime.datetime.now())
        hashmap=hashlib.sha224(username + dateandtime).hexdigest()
        files=open(os.path.abspath('Devil/files.txt'),'U')
        lines=files.readlines();
        #os.makedirs(os.path.abspath('Devil')+'/object'+'/'+hashmap)
        for line in lines:
                #print line
                path=line.split(" ")
                if(path[1]=="notcommited\n"):
                        if(os.path.isfile(path[0])== True):
                                #print "in file ",path[0]
                                if not (os.path.exists(os.path.abspath('Devil')+'/object'+'/'+hashmap)):
                                        os.makedirs(os.path.abspath('Devil')+'/object'+'/'+hashmap)
                                shutil.copy2(path[0],os.path.abspath('Devil')+'/object'+'/'+hashmap)
                        elif(os.path.isdir(path[0])== True):
                                print("in dir")
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
                except OSError(e):
                            raise


    def clone(self,target):
        pass

    def log(self):
	#uname=open(self.directory + '/Devil/'+'username.txt','U')
	username,email=getUsername(self.userfile)
	#uname.close()
	for files in os.listdir(os.path.abspath('Devil')+'/object'):
		fordate=os.path.getmtime(os.path.abspath('Devil')+'/object/'+files)
		date=datetime.datetime.fromtimestamp(int(fordate)).strftime('%Y-%m-%d %H:%M:%S')
		print "Commit tag: ",str(files),"\n"
		print "Author: ",username,email"\n"
		print "Time Stamp: ",date,"\n\n"


    def diff(self,commit1,commit2):
        dir1=os.path.abspath(os.path.join(self.objectdir,commit1))
	dir2=os.path.abspath(os.path.join(self.objectdir,commit2))
	dc=filecmp.dircmp(dir1,dir2)
	dc.report_full_closure()

    def status(self):
        files=open(self.statusfile)
	lines=files.readlines();
	for line in lines:
		print line

    def pull(self,url):
        pass

    def push(self,url):
        pass

    def revert(self,commit_hash):
        pass

    # Helpers
    def __objectname(hashtag):
        return os.path.join(self.objectdir,hashtag)

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--init", help = "Initialize the repo", dest="init",action= "store_true")
    parser.add_option("-a", "--add", help = "add files to tracking system", dest="add",action= "store")
    parser.add_option("-c", "--commit",help="commit the required changes", dest="commit",action= "store")
    parser.add_option("-s", "--status",help="all not commited files", dest="status",action= "store_true")
    parser.add_option("-l", "--log",help="complete list of commits", dest="log",action= "store_true")
    parser.add_option("-d", "--diff",help="overview of difference", dest="diff",action= "store")
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
    elif options.diff:
	clist=options.diff.split("..")
	obj=FileController()
	obj.diff(clist[0],clist[1])

if __name__ == "__main__":
    main()
