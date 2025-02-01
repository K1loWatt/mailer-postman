import sys
import os
import json
from postman.connector import Gmail
from postman.mail import Mail
from postman.manager import Manager


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


def run(msg: str, subject: str, destination: str) -> None:
    config = load_config()
    conn = Gmail(
        config.get("username"),
        config.get("pass"),
        config.get("host"),
        config.get("port"),
        config.get("tls"),
    )
    manager = Manager(conn)
    mail = Mail(msg, subject)
    manager.send(mail, destination)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: my_executable.exe <destination> <subject> <message>")
        sys.exit(1)

    destination = sys.argv[1]
    subject = sys.argv[2]
    msg = sys.argv[3]

    run(msg, subject, destination)
