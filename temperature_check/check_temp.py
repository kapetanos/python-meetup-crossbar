import re
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet import utils
from autobahn.twisted.util import sleep

class Component(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        while True:
            try:
                #output = yield utils.getProcessOutput('/usr/bin/vcgencmd', args=('measure_temp',))
                output = yield utils.getProcessOutput('vcgencmd', args=('measure_temp',))
            except:
                print('Could not run process!')
                yield sleep(60)
                continue

            print(output)
            m = re.match(r'temp=(.*)\'C', output.decode('utf-8'))

            if m:
                temperature = float(m.group(1))
                if temperature > 75:
                    try:
                        yield self.call('notify_owner', temperature)
                    except:
                        print('Error while calling notify_owner')

            yield sleep(300)

if __name__ == '__main__':
    realm = 'realm1'
    runner = ApplicationRunner('ws://127.0.0.1:8080/ws', realm)
    runner.run(Component)
