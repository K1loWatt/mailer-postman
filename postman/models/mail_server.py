from abc import ABC, abstractmethod
import sys
import os
import json
from postman.models.mail import Mail
import smtplib
import socket
import time
from typing import Callable
from dataclasses import dataclass, field
import argparse
from dotenv import load_dotenv


@dataclass
class Config:
    host: str
    username: str
    password: str
    port: int
    tls: bool


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
        if self.config.tls:
            self.server.starttls()
        self.server.login(self.config.username, self.config.password)
        self.server.sendmail(
            self.config.username, mail.destination, mail.content.encode("utf-8")
        )

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.server:
            self.server.__exit__(exc_type, exc_val, exc_tb)

