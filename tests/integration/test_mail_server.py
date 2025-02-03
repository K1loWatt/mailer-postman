import pytest
from postman.models.mail_server import SMTPServer, Config
from postman.models.mail import Mail
from tests.conftest import FAKE_MAIL, FAKE_PASS
import smtplib
import requests

def get_mailhog_messages():
    """Fetch emails from MailHog."""
    response = requests.get("http://localhost:8025/api/v2/messages")
    response.raise_for_status()
    return response.json()

def test_smtp_server():

    config = Config("localhost", FAKE_MAIL, FAKE_PASS, 1025, False)
    mail_server = SMTPServer(config)
    assert mail_server.config == config
    
    mail = Mail("Hello", "Test", "destination")
    with SMTPServer(config) as server:
        server.send_mail(mail)
        
    messages = get_mailhog_messages()
    assert len(messages["items"]) == 1
    assert messages["items"][0]["Raw"]["From"] == "test@localhost.com"
    assert messages["items"][0]["Raw"]["To"] == ["destination"]
    assert messages["items"][0]["Raw"]["Data"] == mail.content

"""
class MailServer(ABC):
    @abstractmethod
    def __enter__(self) -> "MailServer":
        raise NotImplementedError

    @abstractmethod
    def send_mail(self, mail: Mail) -> None:
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        raise NotImplementedError


class SMTPServer(MailServer):
    server: smtplib.SMTP
    config: Config

    def __init__(self, config) -> None:
        self.config = config

    def __enter__(self) -> "SMTPServer":
        self.server = smtplib.SMTP(self.config.host, self.config.port)
        return self

    def send_mail(self, mail: Mail) -> None:
        self.server.starttls()
        self.server.login(self.config.username, self.config.password)
        self.server.sendmail(
            self.config.username, destination, mail.content.encode("utf-8")
        )

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.server:
            self.server.__exit__(exc_type, exc_val, exc_tb)


"""