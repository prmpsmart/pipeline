import logging


OTP_TIMEOUT_MINUTES = 5

OTP_TIMEOUT = 60 * OTP_TIMEOUT_MINUTES

SESSION_TIMEOUT = 24 * 60 * 60
REFRESH_SESSION_TIMEOUT = 7

GMAIL_REFRESH_TIMEOUT = 30

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiam9obl9kb2UiLCJleHAiOjE3MDM4MjY2Mjl9.joFEjOmttG-j9jIq5il9fnDD4sBYnJtWOZl-lHGnEss"

FROM_EMAIL = "pipelinepayments@gmail.com"

FROM_NAME = "Pipeline"

TOKEN_PICKLE = "src/constants/token.pickle"

CREDENTIALS_JSON = "google_client_secret.json"

FIREBASE_PROJECT_ID = "pipeline-backend"

SERVICE_ACCOUNT_JSON = f"{FIREBASE_PROJECT_ID}-firebase-adminsdk.json"


logging.basicConfig(level=logging.NOTSET)

LOGGER = logging.getLogger("  ")


# p Cashflow,45