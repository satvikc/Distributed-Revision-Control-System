#!/usr/bin/env python
import os
from twisted.spread import pb
from twisted.internet import reactor
from file import FileController
class DevilClient(pb.Root):
   def connect(self):
        clientfactory = pb.PBClientFactory()
        reactor.connectTCP("localhost", 8789, clientfactory)
        d = clientfactory.getRootObject()
        d.addCallback(self.got_connected)


   def got_connected(self,result):
        obj=FileController(os.getcwd())
        d=result.callRemote("getCommits",obj.directory)
        d.addCallback(self.gotCommits)

   def gotCommits(self,commits):
        obj=FileController(os.getcwd())
        mycommits = obj.getAllCommits()
        commits_to_fetch = set(commits).difference(set(mycommits))
        d.addCallBack(self.forLoop,commits_to_fetch)

   def forLoop(self,commits_to_fetch,commits,mycommits):
        if(len(commits_to_fetch)>0):
            i = commits_to_fetch[0].split()
            committag = i[1]
            print(committag)
            d.addCallBack(self.forLoop2,commits_to_fetch[1:],commits,mycommits)
        else:
            d=commits.callRemote("getCommitsContent",committag)
            d.addCallBack(self.gotCommitsContent,commits,mycommits)

   def forLoop2(self,commits_to_fetch,commits,mycommits):
        obj=FileController(os.getcwd())
        fp = open(obj.statusfile,'a')
        obj=FileController(os.getcwd())
        obj.uncompressAndWrite(committag,cont)
        # add to status file
        print(k)
        fp.write(k)
        if(len(commits_to_fetch)>0):
            i = commits_to_fetch[0].split()
            committag = i[1]
            print(committag)
            d.addCallBack(self.forLoop2,commits_to_fetch[1:],commits,mycommits)
        else:
            d=commits.callRemote("getCommitsContent",committag)
            d.addCallBack(self.gotCommitsContent,commits,mycommits)

   def gotCommitsContent(self,cont,commits,mycommits):
        fp.close()
        parent_commit=[x for x in commits if x in set(mycommits)][-1]
        #print (parent_commit.split()[1])
        parent_file_list=obj.getFileList(parent_commit.split()[1])
        my_file_list=obj.getFileList(mycommits[-1].split()[1])
        other_file_list=obj.getFileList(commits[-1].split()[1])
        flag=0
        for elem in my_file_list:
                for temp in other_file_list:
                        if(elem==temp):
                                dicts=merge3.devilMerge(obj.getFile(parent_commit.split()[1],elem[0]),obj.getFile(mycommits[-1].split()[1],elem[0]),obj.getFile(commits[-1].split()[1],elem[0]))
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
