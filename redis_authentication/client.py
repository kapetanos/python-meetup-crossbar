import os
import sys

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession

CLIENT_NAME = 'one'
CLIENT_TICKET = 'correct'

class ClientSession(ApplicationSession):

   def onConnect(self):
      print("Client session connected. Starting WAMP-Ticket authentication on realm '{}' as principal '{}' ..".format(self.config.realm, CLIENT_NAME))
      self.join(self.config.realm, ["ticket"], CLIENT_NAME)

   def onChallenge(self, challenge):
      if challenge.method == "ticket":
         print("WAMP-Ticket challenge received: {}".format(challenge))
         return CLIENT_TICKET
      else:
         raise Exception("Invalid authmethod {}".format(challenge.method))

   @inlineCallbacks
   def onJoin(self, details):
      print("Client session joined: {}".format(details))

      yield self.leave()


   def onLeave(self, details):
      print("Client session left: {}".format(details))
      self.disconnect()

   def onDisconnect(self):
      print("Client session disconnected.")
      reactor.stop()


if __name__ == '__main__':

   from autobahn.twisted.wamp import ApplicationRunner

   runner = ApplicationRunner(url=u'ws://localhost:8080/ws', realm=u'realm1')
   runner.run(ClientSession)
