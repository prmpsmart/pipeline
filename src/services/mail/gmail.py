from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from email.utils import formataddr

import os
import pickle
import time

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from ...constants.config import *

from ...utils.base import SingletonChild
from ...utils.commons import run_on_thread


# Request all access (permission to read/send/receive emails, manage the inbox, and more)


class GmailSend(SingletonChild):
    def __init__(
        self,
        from_email: str = FROM_EMAIL,
        from_name: str = FROM_NAME,
        token_pickle: str = TOKEN_PICKLE,
        credentials_json: str = CREDENTIALS_JSON,
        scopes: list[str] = ["https://www.googleapis.com/auth/gmail.send"],
    ):
        super().__init__()

        self.from_email = from_email
        self.from_name = from_name
        self.credentials_json = credentials_json
        self.scopes = scopes
        self.token_pickle = token_pickle

        self.creds: Credentials = None
        self.service = None

    def setup(self):
        if os.path.exists(self.token_pickle):
            with open(self.token_pickle, "rb") as token:
                self.creds = pickle.load(token)

        # if there are no (valid) credentials availablle, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.refresh_token()
                except:
                    self.run_flow()
            else:
                self.creds = self.run_flow()

        self.service = build("gmail", "v1", credentials=self.creds)

        run_on_thread(self.refresh_on_loop)

    def refresh_token(self):
        self.creds.refresh(Request())
        self.dump_token()
        LOGGER.debug("GMail Token Refreshed and Persisted.")

    def refresh_on_loop(self):
        start_time = time.time()
        duration = 60 * GMAIL_REFRESH_TIMEOUT

        while self.alive:
            if time.time() - start_time >= duration:
                self.refresh_token()
                start_time = time.time()

    def run_flow(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credentials_json,
            self.scopes,
        )
        self.creds = flow.run_local_server(port=0)
        self.dump_token()

    def dump_token(self):
        with open(self.token_pickle, "wb") as token:
            pickle.dump(self.creds, token)

    def send(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        body: str,
    ):
        message = MIMEText(body, _subtype="html")
        message["to"] = formataddr((to_name, to_email))
        message["from"] = formataddr((self.from_name, self.from_email))
        message["subject"] = subject

        if self.service:
            return (
                self.service.users()
                .messages()
                .send(
                    userId="me",
                    body={
                        "raw": urlsafe_b64encode(message.as_bytes()).decode(),
                    },
                )
                .execute()
            )

    def send_otp(
        self,
        to_email: str,
        to_name: str,
        otp: int,
    ):
        return self.send(
            to_email,
            to_name,
            f"Account Verification OTP from {FROM_NAME}",
            f"<html><body>Your {FROM_NAME} Account Verification OTP is <h1>{otp}</h1>Valid for {OTP_TIMEOUT_MINUTES} minutes.</body></html>",
        )

    def send_reset_otp(
        self,
        to_email: str,
        to_name: str,
        otp: int,
    ):
        return self.send(
            to_email,
            to_name,
            f"Password Reset OTP from {FROM_NAME}",
            f"Your {FROM_NAME} Password Reset OTP is <h1>{otp}</h1>Valid for {OTP_TIMEOUT_MINUTES} minutes.",
        )


GmailSend = GmailSend()
