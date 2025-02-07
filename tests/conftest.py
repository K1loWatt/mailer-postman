from postman.models.mail_server import MailServer
from postman.models.mail import Mail
from dataclasses import dataclass


FAKE_MAIL = "test@localhost.com"
FAKE_PASS = "pass"


@dataclass
class FakeMailServer(MailServer):
    mail_sent: bool = False

    def __enter__(self):
        return self

    def send_mail(self, mail: Mail):
        self.mail_sent = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
