#!/usr/bin/env python
import os
from twisted.spread import pb
from twisted.internet import reactor
from file import FileController
from file import merge3
from file import getLastCommit
class DevilClient(pb.Root):
   def connect(self):
        clientfactory = pb.PBClientFactory()
        reactor.connectTCP("localhost", 6001, clientfactory)
        d = clientfactory.getRootObject()
        d.addCallback(self.got_connected)


   def got_connected(self,result):
        self.result=result
        obj=FileController(os.getcwd())
        d=result.callRemote("getCommits","../devil2")
        d.addCallback(self.gotCommits)

   def gotCommits(self,commits):
        obj=FileController(os.getcwd())
        mycommits = obj.getAllCommits()
        print commits,"\n"
        print mycommits,"\n"
        commits_to_fetch = set(commits).difference(set(mycommits))
        fp = open(obj.statusfile,'a')
        for k in commits_to_fetch:
            fp.write(k)
        fp.close()
        c_to_fetch = [i.split()[1] for i in commits_to_fetch]
        print c_to_fetch
        if c_to_fetch == []:
                reactor.stop()
        else:
                d=self.result.callRemote("getCommitContent","../devil2",c_to_fetch)
                d.addCallback(self.gotCommitsContent,commits,mycommits)

   def gotCommitsContent(self,cont,commits,mycommits):
        obj=FileController(os.getcwd())
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
        for elem in my_file_list:
                for temp in other_file_list:
                        if(elem[0]==temp[0]):
                                dicts=merge3.devilMerge(obj.getFile(getLastCommit(common_commit),elem[0]),obj.getFile(getLastCommit(mycommits),elem[0]),obj.getFile(getLastCommit(commits),elem[0]))
                                #print dicts
                                #reactor.stop()
                                
                                print "opening file ",elem[0]
                                files=open(elem[0],'w')
                                files.write(dicts['md_content'])
                                files.close()
                                
                                if(dicts['conflict']==0 and dicts['merged']!=0):
                                        print("Merged "+elem[0]+"\n")
                                else:
                                        print("Merged with conflicts in "+elem[0]+" not commiting.Please commit after manually changing")
                                        flag=1
        if(flag==0):
                obj.commit('auto-merged successfull')
        reactor.stop()

if __name__ == '__main__':
    DevilClient().connect()
    reactor.run()

