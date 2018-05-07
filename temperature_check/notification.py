from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.mail.smtp import sendmail
from email.mime.text import MIMEText
import mail_config as mc #just a module containing the credentials

class NotificationComponent(ApplicationSession):
    @inlineCallbacks
    def send_notification(self, temperature):
        message = MIMEText('The temperature is {}!'.format(temperature))
        message["Subject"] = "RPi Temperature warning!"
        message["From"] = mc.ME
        message["To"] = ", ".join(mc.TO)

        yield sendmail(mc.SERVER, mc.ME, mc.TO, message,
                       requireAuthentication=True,
                       requireTransportSecurity=True,
                       port=mc.PORT, username=mc.USERNAME, password=mc.PASSWORD)

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.send_notification, 'notify_owner')

if __name__ == '__main__':
    realm = 'realm1'
    runner = ApplicationRunner('ws://127.0.0.1:8080/ws', realm)
    runner.run(NotificationComponent)
