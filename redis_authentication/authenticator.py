import os
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError

import txredisapi as redis

from pprint import pprint

class AuthenticatorSession(ApplicationSession):

    @inlineCallbacks
    def authenticate(self, realm, authid, details):
        ticket = details['ticket']
        print("WAMP-Ticket dynamic authenticator invoked: realm='{}', authid='{}', ticket='{}'".format(realm, authid, ticket))
        pprint(details)
    
        rc = yield redis.Connection()

        redis_ticket = yield rc.get(authid)

        if ticket == redis_ticket:
            return 'regular_client'
        else:
            raise ApplicationError("com.example.invalid_ticket", "could not authenticate session - invalid ticket '{}' for user {}".format(ticket, authid))

    @inlineCallbacks
    def onJoin(self, details):
       try:
           yield self.register(self.authenticate, 'com.example.authenticate')
           print("WAMP-Ticket dynamic authenticator registered!")
       except Exception as e:
           print("Failed to register dynamic authenticator: {0}".format(e))

