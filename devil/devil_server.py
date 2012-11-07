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


        


if __name__ == '__main__':
    serverfactory = pb.PBServerFactory(DevilServer())
    reactor.listenTCP(6001, serverfactory)
    reactor.run()

