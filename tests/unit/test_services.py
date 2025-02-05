import pytest
from postman.models.mail import Mail
from postman.models.mail_server import MailServer
from postman.services.services import send_mail_with_retry, send_mail
import socket
from unittest.mock import MagicMock
from tests.conftest import FakeMailServer


def test_send_mail():
    mail = Mail("Hello", "Test", "destination")
    mail_server = FakeMailServer()
    send_mail(mail, mail_server)
    assert mail_server.mail_sent == True


def test_send_mail_with_retry():
    mail = Mail("Hello", "Test", "destination")
    mail_server = FakeMailServer()

    mail_server.send_mail = MagicMock(side_effect=socket.gaierror)

    with pytest.raises(socket.gaierror):
        send_mail_with_retry(mail, mail_server, 10, 0.01)

    assert mail_server.send_mail.call_count == 10
