from postman.models.mail import Mail


def test_mail():
    mail = Mail("Hello", "Test", "destination")
    assert str(mail) == "Subject: Test"
    assert mail.content == "Subject: Test\n\nHello"
    assert mail.destination == "destination"
