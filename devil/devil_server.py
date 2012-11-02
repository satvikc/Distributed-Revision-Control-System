from twisted.spread import pb
from twisted.internet import reactor
from file import FileController 

class DevilServer(pb.Root):
    def remote_getCommits(self,directory):
        f = FileController(directory)
        return f.getAllCommits()

    def remote_getCommitContent(self,directory,commit):
        f = FileController(directory)
        return f.compressAndSend(commit)

    def remote_push(self,directory,loc):
        print loc,"\n"
        print directory
        print "received push request"
        f = FileController(directory)
        f.pull(loc)
        print "pull completed"
        return 1

if __name__ == '__main__':
    serverfactory = pb.PBServerFactory(DevilServer())
    reactor.listenTCP(7001, serverfactory)
    #serverfactory2 = pb.PBServerFactory(DevilServer())
    #reactor.listenTCP(7001, serverfactory2)
    reactor.run()

