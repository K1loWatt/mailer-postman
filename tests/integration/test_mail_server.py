from postman.models.mail_server import SMTPServer, Config
from postman.models.mail import Mail
from tests.conftest import FAKE_MAIL, FAKE_PASS

import requests


def get_mailhog_messages():
    """Fetch emails from MailHog."""
    response = requests.get("http://localhost:8025/api/v2/messages")  # mypy: ignore
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

