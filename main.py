import sys
import os
import json
from postman.mail import Mail
import smtplib
import socket
import time
from typing import Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import argparse


def get_base_path():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def load_config() -> dict[str, str]:
    base_path = get_base_path()
    config_path = os.path.join(base_path, "config.json")

    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    return config


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

    def __init__(self, config) -> None:
        self.config = config

    def __enter__(self) -> "SMTPServer":
        self.server = smtplib.SMTP(self.config)
        return self

    def send_mail(self, mail: Mail) -> None:
        self.server.starttls()
        self.server.login(self.config.get("username"), self.config.get("pass"))
        self.server.sendmail(
            self.config.get("username"), destination, mail.content.encode("utf-8")
        )

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.server:
            self.server.__exit__(exc_type, exc_val, exc_tb)


def send_mail_with_retry(mail: Mail, mail_server: MailServer) -> None:
    while True:
        try:
            send_mail(mail, mail_server)
            break
        except socket.gaierror:
            print("Error connecting to server, retrying in 60 seconds")
            time.sleep(60)


def send_mail(mail: Mail, mail_server: MailServer) -> None:
    with mail_server as server:
        server.send_mail(mail)


def run(msg: str, subject: str, destination: str, retry: bool) -> None:
    config = load_config()
    mail_server = SMTPServer(config)
    mail = Mail(msg, subject, destination)
    send_mail(mail, mail_server) if not retry else send_mail_with_retry(
        mail, mail_server
    )


if __name__ == "__main__":
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

    run(msg, subject, destination, retry)
