from src.shared.services.mail.gmail import GmailSend


g = GmailSend()
g.send(
    to_email="prmpsmart@mailinator.com",
    to_name="PRMPSmart",
    subject="Test Fuitos Mail",
    body="This is a test email for Fuitos App",
)
