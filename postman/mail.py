from dataclasses import dataclass


@dataclass
class Mail:
    body: str
    subject: str

    @property
    def content(self) -> str:
        return f"Subject: {self.subject}\n\n{self.body}"

    def __str__(self) -> str:
        return f"Subject: {self.subject}"
