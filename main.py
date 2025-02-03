import os
from postman.models.mail import Mail

import argparse
from dotenv import load_dotenv
from postman.models.mail_server import SMTPServer, Config
from postman.services.services import send_mail, send_mail_with_retry


def run(msg: str, subject: str, destination: str, retry: bool, config: Config) -> None:
    mail_server = SMTPServer(config)
    mail = Mail(msg, subject, destination)
    send_mail(mail, mail_server) if not retry else send_mail_with_retry(
        mail, mail_server
    )


if __name__ == "__main__":
    load_dotenv()

    # "username": "<mail@mail.com>",
    # "pass": "<password>",
    # "host": "smtp.gmail.com", #for Gmail
    # "port": 587, #for Gmail

    smtp_server = os.getenv("SMTP_SERVER")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    port = os.getenv("SMTP_PORT")
    tls = os.getenv("TLS")
    assert smtp_server and username and password and port and tls
    config = Config(smtp_server, username, password, int(port), bool(tls))
    parser = argparse.ArgumentParser(description="Send an email using the SMTP server.")
    parser.add_argument("destination", type=str, help="The email destination address.")
    parser.add_argument("subject", type=str, help="The subject of the email.")
    parser.add_argument("message", type=str, help="The message content of the email.")
    parser.add_argument(
        "--retry",
        action="store_true",
        help="Retry sending the email on failure.",
        default=False,
    )

    args = parser.parse_args()

    destination = args.destination
    subject = args.subject
    msg = args.message
    retry = args.retry

    run(msg, subject, destination, retry, config)
