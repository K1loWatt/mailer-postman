from postman.models.mail_server import Mail, MailServer
from postman.models.mail import Mail
import socket
import time
from typing import Tuple

def send_mail_with_retry(mail: Mail, mail_server: MailServer, number_of_retries:int, retry_delay:float) -> None:
    
    for _ in range(number_of_retries):
        try:
            send_mail(mail, mail_server)
            break
        except socket.gaierror as exec:
            print(f"Error connecting to server, retrying in {retry_delay} seconds")
            time.sleep(retry_delay)
            if _ == number_of_retries-1:
                raise exec


def send_mail(mail: Mail, mail_server: MailServer) -> None:
    with mail_server as server:
        server.send_mail(mail)