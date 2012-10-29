from twisted.spread import pb
from twisted.application.internet import TCPServer
from twisted.application.service import Application

class DevilRemote(pb.Root):
    def remote_get_versions(self,uname):
        return 0

serverfactory = pb.PBServerFactory(DevilRemote())
application = Application("remote")
serverService = TCPServer(8789, serverfactory)
serverService.setServiceParent(application)
