import sys
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.task import LoopingCall

class Component(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        def got_message(msg):
            print('Got message: {}'.format(msg))

        # Subscribe to the hello.topic topic to receive messages
        yield self.subscribe(got_message, 'hello.topic')

        # Publish "Hello, world!" message to the hello.topic topic
        def publish():
            return self.publish('hello.topic', 'Hello, world! My name is {}!'.format(sys.argv[1]))
        LoopingCall(publish).start(1)

if __name__ == '__main__':
    realm = 'realm1'
    runner = ApplicationRunner('ws://127.0.0.1:8080/ws', realm)
    runner.run(Component)
