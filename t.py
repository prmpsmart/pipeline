from src.constants.config import FROM_NAME
from src.services.mail.gmail import GmailSend


g = GmailSend
g.setup()
g.send(
    to_email="prmpsmart@mailinator.com",
    to_name="PRMPSmart",
    subject=f"Test {FROM_NAME} Mail",
    body=f"This is a test email for {FROM_NAME} App",
)
