from twisted.spread import pb
from twisted.application.internet import TCPClient
from twisted.application.service import Application

class DevilClient(object):
    def get_versions(self, result):
        d = result.callRemote("get_versions", "all")
        d.addCallback(self.got_versions)

    def got_versions(self, result):
        print "server echoed: ", result

e = DevilClient()
clientfactory = pb.PBClientFactory()
d = clientfactory.getRootObject()
d.addCallback(e.get_versions)

application = Application("client")
echoClientService = TCPClient("localhost", 8789, clientfactory)
echoClientService.setServiceParent(application)
