#! /usr/bin/python2
import exceptions,os,shutil,hashlib,datetime,filecmp,base64,difflib,sys,zlib,tempfile,merge3
from optparse import OptionParser
from utils import fileTracked,getUsername,getHashNameFromHashmap
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
from twisted.spread import pb
from twisted.internet import reactor

class DevilClientPush(pb.Root):
   def connect(self,directory,ip,port,sdirectory,selfip,selfport):
        self.directory=directory
        clientfactory = pb.PBClientFactory()
        reactor.connectTCP(ip, port, clientfactory)
        d = clientfactory.getRootObject()
        d.addCallback(self.got_connected,sdirectory,selfip,selfport)


   def got_connected(self,result,sdirectory,selfip,selfport):
        loc=selfip+":"+str(selfport)+sdirectory
        d=result.callRemote("push",self.directory,loc)
        d.addCallback(self.got_push)

   def got_push(self,w):
        reactor.stop()

class DevilClient(pb.Root):
   def connect(self,directory,ip,port,sdirectory,stop):
        self.stop = stop
        self.directory=directory
        clientfactory = pb.PBClientFactory()
        reactor.connectTCP(ip, port, clientfactory)
        d = clientfactory.getRootObject()
        d.addCallback(self.got_connected,sdirectory)


   def got_connected(self,result,sdirectory):
        self.result=result
        obj=FileController(self.directory)
        #print str(self.directory=directory)
        d=result.callRemote("getCommits",sdirectory)
        d.addCallback(self.gotCommits,sdirectory)

   def gotCommits(self,commits,sdirectory):
        obj=FileController(self.directory)
        mycommits = obj.getAllCommits()
        #print commits,"\n"
        #print mycommits,"\n"
        commits_to_fetch = set(commits).difference(set(mycommits))
        fp = open(obj.statusfile,'a')
        for k in commits_to_fetch:
            fp.write(k)
        fp.close()
        c_to_fetch = [i.split()[1] for i in commits_to_fetch]
        #print c_to_fetch
        if c_to_fetch == [] and self.stop:
                reactor.stop()
        else:
                d=self.result.callRemote("getCommitContent",sdirectory,c_to_fetch)
                d.addCallback(self.gotCommitsContent,commits,mycommits)

   def gotCommitsContent(self,cont,commits,mycommits):
        obj=FileController(self.directory)
        #print ">>>",self.directory,"<<<"
        obj.uncompressAndWrite(cont)
        common_commit=[x for x in commits if x in set(mycommits)]
        #print getLastCommit(common_commit),"\n"
        #print (parent_commit.split()[1])
        parent_file_list=obj.getFileList(getLastCommit(common_commit))
        my_file_list=obj.getFileList(getLastCommit(mycommits))
        #print my_file_list,"\n"
        other_file_list=obj.getFileList(getLastCommit(commits))
        #print other_file_list,"\n"
        flag=0
        for elem in other_file_list:
                if(elem[0] in [x[0] for x in my_file_list]):
                        dicts=merge3.devilMerge(obj.getFile(getLastCommit(common_commit),elem[0]),obj.getFile(getLastCommit(mycommits),elem[0]),obj.getFile(getLastCommit(commits),elem[0]))
                        #print dicts
                        #reactor.stop()
                        #print str(dicts)
                        #print "opening file ",elem[0]
                        #print os.getcwd()
                        #print elem[0]
                        try:
                                os.makedirs(os.path.dirname(elem[0]))
                        except:
                                pass
                        files=open(elem[0],'w')
                        files.write(dicts['md_content'])
                        files.close()
                        #obj.add(elem[0])
                        if(dicts['conflict']==1):
                                print("Merged with conflicts in "+elem[0]+" not commiting.Please commit after manually changing")
                                flag=1
                        else:
                                        print("Merged "+elem[0]+" successfully\n")
                else:
                        #print "Writing to elem[0]"
                        try:
                                os.makedirs(os.path.dirname(elem[0]))
                        except:
                                pass
                        files=open(elem[0],'w')
                        content=obj.getFiler(getLastCommit(commits),elem[0])
                        files.write(content)
                        files.close()
                        #print elem[0]
                        obj.add(elem[0])
                        
        if(flag==0):
                obj.commit('auto-merged successfull')
        print "Pull Successfull\n"
        if self.stop:
            reactor.stop()



class FileController(object):
    """
    Class to perform all the local functionalities of the version
    control system.
    """
    def __init__(self,dirc):
        """
        Args:
          directory(str): Full path of the directory where the
          version control is initiated.
        Returns:
          FileController Object
        """
        self.directory = dirc
        os.chdir(dirc)
        self.statusfile = os.path.join(self.directory,'Devil','status.txt')
        self.userfile=os.path.join(self.directory,'Devil','username.txt')
        self.trackingfile=os.path.join(self.directory,'Devil','files.txt')
        self.objectdir = os.path.join(self.directory,'Devil','object')
        self.devil=os.path.join(self.directory,'Devil')
        self.commitfiles=os.path.join(self.directory,'Devil','object','commitfiles')
        self.remotefile=os.path.join(self.directory,'Devil','remotefile.txt')

    def start(self):
        """
        Initiates the repository
        """

        try:
                os.makedirs(self.devil)
                username = raw_input("Enter username:\n")
                email = raw_input("Enter email \n")
                uname=open(self.userfile,'w')
                uname.write(username+'\n')
                uname.write(email+'\n')
                uname.close()
                files=open(self.trackingfile,'w')
                files.close()
                files=open(self.statusfile,'w')
                files.close()
                files=open(self.remotefile,'w')
                files.write("[Remotes]\n")
                files.close()
                os.makedirs(os.path.join(self.commitfiles))
        except :
                print "Directory already initiated, cannot initiate again!"
    def start2(self,username,email):
        """
        Initiates the repository
        """

        try:
                os.makedirs(self.devil)
                uname=open(self.userfile,'w')
                uname.write(username+'\n')
                uname.write(email+'\n')
                uname.close()
                files=open(self.trackingfile,'w')
                files.close()
                files=open(self.statusfile,'w')
                files.close()
                files=open(self.remotefile,'w')
                files.write("[Remotes]\n")
                files.close()
                os.makedirs(os.path.join(self.commitfiles))
        except :
                print "Directory already initiated, cannot initiate again!"

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
        relpath = filename
        #print "FILE>>",filename
        #filename = os.path.relpath(filename,self.directory)
        #print "ABSPATH >>",filename
        #relpath = os.path.relpath(filename,self.directory)
        #print "RELP>>",relpath
        if(os.path.isdir(filename)):
            for i in os.listdir(filename):
                self.add(os.path.join(filename,i))
        else:
            if(fileTracked(relpath,self.trackingfile)):
                print(relpath + " => File added to tracking")
                files=open(self.trackingfile,'a')
                files.write( relpath + " notcommited\n")
                files.close()
            else:
                print(relpath + " => File already tracked")

        self.update_modify_time()

    def update_modify_time(self):
        fp = open(self.trackingfile,'r')
        cont = fp.readlines()
        #print str(cont)
        fp.close()
        fp = open(self.trackingfile,'w')
        for i in cont:
            split = i.split()
            name = split[0]
            status = split[1]
            if os.path.isabs(name):
                name = os.path.relpath(name,self.directory)
            fp.write(name + " " + status + " " + str(os.path.getmtime(name))+'\n')
        fp.close()


    def commit(self,message):
        username,email = getUsername(self.userfile)
        dateandtime=str(datetime.datetime.now())
        hashmap=hashlib.sha224(base64.b64encode((username+email+dateandtime).encode('ascii'))).hexdigest()
        files=open(self.trackingfile,'r')
        lines=files.readlines()
        #print "LINES >>",lines
        files.close()
        #os.makedirs(os.path.abspath('Devil')+'/object'+'/'+hashmap)
        if not (os.path.exists(os.path.join(self.commitfiles))):
            os.makedirs(os.path.join(self.commitfiles))
        files=open(os.path.join(self.objectdir,hashmap),'w')
        files.close()
        for line in lines:
                #print line
                path=line.split()
         
                if(path[1]=="notcommited" or path[1]=="commited"):
                        if(os.path.isfile(path[0])== True):
                                #print "in file ",path[0]
                                files=open(path[0],'r')
                                content=files.readlines()
                                files.close()
                                newhashmap=hashlib.sha224(base64.b64encode((str(content)).encode('ascii'))).hexdigest()
                                files=open(os.path.join(self.objectdir,hashmap),'a')
                                files.write(path[0]+"   "+newhashmap+"\n")
                                files.close()
                                shutil.copy2(path[0],os.path.join(self.commitfiles,newhashmap))
                        elif(os.path.isdir(path[0])== True):
                                #print("in dir")
                                shutil.copytree(path[0],os.path.join(self.commitfiles))
        files=open(self.trackingfile,'w')
        for line in lines:
                path = line.split()
                #relpath = os.path.relpath(path[0],self.directory)
                #print "RELPATH>>",relpath," PATH0>> ",path[0]
                files.write( path[0] + " commited\n")
        files.close()
        files=open(self.statusfile,'a')
        files.write("commit "+hashmap+" "+username+" "+email+" "+dateandtime+" "+message+"\n")
        files.close()
        self.update_modify_time()

    def rename(self,newname):
        if os.path.exists(newname):
                raise DirectoryExist
        else:
                try:
                            os.rename(self.directory, newname)
                except OSError(e):
                            raise



    def clone(self,target):
        print "not implemented\n"
        #sdirectory=target.split(":")[1][4:]
        #self.directory = os.path.basename(sdirectory)
        #self.start()
        #self.pull(target)

    def status(self):
        files=open(self.trackingfile)
        lines=files.readlines();
        splitted = [(l[0],l[1],l[2]) for l in (y.split() for y in lines)]
        for (f,st,md) in splitted:
            if st != 'commited':
                print("added: " + f)
            elif not (md == str(os.path.getmtime(f))):
                print("modified: " + f)


    def change(self,commit1,commit2):
        dir1=os.path.join(self.objectdir,commit1)
        dir2=os.path.join(self.objectdir,commit2)
        dc=filecmp.dircmp(dir1,dir2)
        dc.report_full_closure()

    def log(self):
        files=open(self.statusfile)
        lines=files.readlines();
        files.close()
        for line in lines:
            line = line.split()
            print("Commit: " + line[1])
            print("Author: " + line[2])
            print("Email: " + line[3])
            print("Date: " + line[4])
            print("Msg: " + ' '.join(line[6:]))
            print '\n'


    def diff(self,filename):
        files=open(self.statusfile,'r')
        a=files.readlines();
        lastline=a[len(a)-1]
        files.close()
        files=open(os.path.join(self.directory,filename),'r')
        b=files.readlines();
        files.close()
        for_commit=lastline.split("commit ")
        commit_tag=for_commit[1].split(" ")[0]
        c=self.getFile(commit_tag,filename)
        for line in difflib.ndiff(c,b):
            print(line[:-1])


    def pull(self,istring,close=True):
        ip=istring.split(":")[0]
        port=int(istring.split(":")[1].split("/")[0])
        sdirectory=istring.split(":")[1][4:]
        #print ip,str(port),sdirectory,"\n"
        DevilClient().connect(self.directory,ip,port,sdirectory,close)
        

    def push(self,istring):
        selfip=istring.split(":")[0]
        #localhost:7000localhost:7001/home/rahulaaj/devil/test
        selfport=int(istring.split(":")[1][0:4])
        ip=istring.split(":")[1][4:]
        port=int(istring.split(":")[2].split("/")[0])
        sdirectory=istring.split(":")[2][4:]
        print selfip,str(selfport),ip,str(port),sdirectory,"\n"
        DevilClientPush().connect(sdirectory,ip,port,self.directory,selfip,selfport)

    def revert(self,commit_hash):
        files=open(os.path.join(self.objectdir,commit_hash),'r')
        a=files.readlines()
        for line in a:
                filename=line.split(" ")[0]
                content=self.getFiler(commit_hash,filename)
                files=open(os.path.join(self.directory,filename),'w')
                files.write(content)
                files.close()


    def merge(self,directory):
        commits = getCommits(directory)
        #print(commits)
        mycommits = self.getAllCommits()
        commits_to_fetch = set(commits).difference(set(mycommits))
        fp = open(self.statusfile,'a')
        for k in commits_to_fetch:
            fp.write(k)
        fp.close()
        c_to_fetch = [i.split()[1] for i in commits_to_fetch]
        cont = getCommitsContent(directory,c_to_fetch)
        self.uncompressAndWrite(cont)
        common_commit=[x for x in commits if x in set(mycommits)]
        #print (parent_commit.split()[1]) 
        parent_file_list=self.getFileList(getLastCommit(common_commit))
        my_file_list=self.getFileList(getLastCommit(mycommits))
        other_file_list=self.getFileList(getLastCommit(commits))
        flag=0
        for elem in my_file_list:
                for temp in other_file_list:
                        if(elem==temp):
                                dicts=merge3.devilMerge(self.getFile(getLastCommit(common_commit),elem[0]),self.getFile(getLastCommit(mycommits),elem[0]),self.getFile(getLastCommit(commits),elem[0]))
                                files=open(elem[0],'w')
                                files.write(dicts['md_content'])
                                files.close()
                                if(dicts['conflict']==0 and dicts['merged']!=0):
                                        print("Merged "+elem[0]+"\n")
                                else:
                                        print("Merged with conflicts in "+elem[0]+" not commiting.Please commit after manually changing")
                                        flag=1
        if(flag==0):
                self.commit('auto-merged successfull')
    # Helpers
    def __objectname(self,hashtag):
        return os.path.join(self.objectdir,hashtag)


    def getFile(self,committag,filename):
        hashmap = os.path.join(self.objectdir,committag)
        h = getHashNameFromHashmap(hashmap,filename)
        try:
            fp = open(os.path.join(self.commitfiles,h),'r')
            content = fp.readlines()
            fp.close()
            return content
        except:
            return ''

    def getFileName(self,committag):
        fp = open(os.path.join(self.objectdir,committag))
        lines = fp.readlines()
        return [l.split()[0] for l in lines]

    def getFileLoc(self,committag,filename):
        fp = open(os.path.join(self.objectdir,committag))
        lines = fp.readlines()
        splits = [i.split() for i in lines]
        for (n,h) in splits:
            if n == filename:
                return h
        return None


    def getFiler(self,committag,filename):
        hashmap = os.path.join(self.objectdir,committag)
        h = getHashNameFromHashmap(hashmap,filename)
        try:
            fp = open(os.path.join(self.commitfiles,h),'r')
            content = fp.read()
            fp.close()
            return content
        except:
            return ''

    def getFileList(self,commit_tag):
        try:
            files=open(os.path.join(self.objectdir,commit_tag),'r')
            lines=files.readlines()
            tlist=[]
            for line in lines:
                line_split=line.split()
                tlist.append((line_split[0],line_split[1]))
            files.close()
            return tlist
        except:
            return []

    def getAllCommits(self):
        fp = open(self.statusfile)
        lines = fp.readlines()
        fp.close()
        return lines

    def compressAndSend(self,commit): #warning doesnot handle empty directory
        archivename = self.compressAll(commit)
        fp = open(archivename,'rb')
        contents = fp.read()
        fp.close()
        return contents

    def compressAll(self,commits):
        tempdir = tempfile.mkdtemp()
        temp = tempfile.gettempdir()
        commitdir = os.path.join(tempdir,os.path.basename(self.commitfiles))
        try:
            os.mkdir(commitdir)
        except:
            pass
        (_,archivename) = tempfile.mkstemp(suffix='.zip')
        for i in commits:
            filenames = self.getFileName(i)
            shutil.copy2(os.path.join(self.objectdir,i),tempdir)
            for fn in filenames:
                h = self.getFileLoc(i,fn)
                floc = os.path.join(self.commitfiles,h)
                shutil.copy2(floc, commitdir)
        zipdir(tempdir,archivename)
        return archivename


    def uncompressAndWrite(self,content):
        (_,archivename) = tempfile.mkstemp(suffix='.zip')
        fp = open(archivename,'wb')
        fp.write(content)
        fp.close()
        unzipdir(self.objectdir,archivename)

# Merge helpers. Remove them when you implement over network.

def getLastCommit(clist):
    try:
        return clist[-1].split()[1]
    except:
        return None

def getCommits(d):
    f = FileController(d)
    return f.getAllCommits()

def getCommitsContent(d,c):
    f = FileController(d)
    return f.compressAndSend(c)

def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)

def unzipdir(targetdir, archivename):
    assert os.path.isdir(targetdir)
    assert os.path.isfile(archivename)
    zip_file = ZipFile(archivename, 'r')
    zip_file.extractall(targetdir)

    zip_file.close()

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--init", help = "Initialize the repo", dest="init",action= "store_true")
    parser.add_option("-a", "--add", help = "add files to tracking system", dest="add",action= "store")
    parser.add_option("-c", "--commit",help="commit the required changes", dest="commit",action= "store")
    parser.add_option("-s", "--status",help="all not commited files", dest="status",action= "store_true")
    parser.add_option("-l", "--log",help="complete list of commits", dest="log",action= "store_true")
    parser.add_option("-d", "--diff",help="Given a file name shows diff from last commit", dest="diff",action= "store")
    parser.add_option("-r", "--revert",help="revert current directory to an old commit", dest="revert",action= "store")
    parser.add_option("--change",help="overview of difference b/w two commits", dest="change",action= "store")
    parser.add_option("-p", "--pull", help = "pull and merge commits and files", dest="pull",action= "store")
    parser.add_option("--push", help = "pushes the commits to the ipport provided", dest="push",action= "store")
    parser.add_option("--clone", help = "clones a target directory into its folder", dest="clone",action= "store")
    (options, args) = parser.parse_args()
    if options.init:
        #print("Initializing repo")
        obj=FileController(os.getcwd())
        obj.start()
    elif options.add:
        obj=FileController(os.getcwd())
        #print options.add
        obj.add(options.add)
    elif options.commit:
        obj=FileController(os.getcwd())
        obj.commit(options.commit)
    elif options.status:
        obj=FileController(os.getcwd())
        obj.status()
    elif options.log:
        obj=FileController(os.getcwd())
        obj.log()
    elif options.change:
        clist=options.change.split("..")
        obj=FileController()
        obj.change(clist[0],clist[1])
    elif options.diff:
        obj=FileController(os.getcwd())
        obj.diff(options.diff)
    elif options.revert:
        obj=FileController(os.getcwd())
        obj.revert(options.revert)
    elif options.pull:
        obj=FileController(os.getcwd())
        obj.pull(options.pull)
        reactor.run()
    elif options.push:
        obj=FileController(os.getcwd())
        obj.push(options.push)
        reactor.run()
    elif options.clone:
        sdirectory=(options.clone).split(":")[1][4:]
        temp=os.path.join(os.getcwd(),os.path.basename(sdirectory))
        os.makedirs(temp)
        obj=FileController(temp)
        obj.start()
        os.chdir(temp)
        obj.pull(options.clone)
        reactor.run()

if __name__ == "__main__":
    main()
