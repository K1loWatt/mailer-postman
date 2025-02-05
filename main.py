import os
from postman.models.mail import Mail

import argparse
from dotenv import load_dotenv
from postman.models.mail_server import SMTPServer, Config
from postman.services.services import send_mail, send_mail_with_retry


def run(
    msg: str,
    subject: str,
    destination: str,
    retry: bool,
    number_of_retries: int,
    retry_delay: int,
    config: Config,
) -> None:
    mail_server = SMTPServer(config)
    mail = Mail(msg, subject, destination)
    send_mail(mail, mail_server) if not retry else send_mail_with_retry(
        mail, mail_server, number_of_retries, retry_delay
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
        help="Number of retries to send the email if failed.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--number-of-retries",
        type=int,
        help="Number of retries to send the email if failed.",
        default=50,
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        help="Retry sending the email if failed.",
        default=60,
    )
    args = parser.parse_args()

    destination = args.destination
    subject = args.subject
    msg = args.message
    retry = args.retry
    number_of_retries = args.number_of_retries
    retry_delay = args.retry_delay

    run(msg, subject, destination, retry, number_of_retries, retry_delay, config)
