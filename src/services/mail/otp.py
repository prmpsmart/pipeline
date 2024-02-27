import random
from ...utils.commons import get_timestamp, hash_bcrypt, run_on_thread
from ...utils.base import Child, modifier
from ...constants.config import *
from ...models import User
from .gmail import GmailSend


class OTP(Child):
    def __init__(self, user: User):
        Child.__init__(self, id=user.email)
        self.user = user
        self.otp: int = 0
        self.verified = user.verified
        self.last_otp_generated_time: int = 0

    @modifier
    def send_otp(self):
        if not self.otp:
            otp = self.generate()
            sent = GmailSend.send_otp(
                self.user.email,
                self.user.full_name,
                otp,
            )
            LOGGER.info(f"{self.user}: VERIFY OTP generated :: {otp}")
            return sent

    @property
    def valid(self) -> bool:
        return (
            self.verified != True
            and (get_timestamp() - self.modified_timestamp) <= OTP_TIMEOUT
        )

    @property
    def timeout(self) -> int:
        if self.valid:
            return OTP_TIMEOUT - get_timestamp() + self.last_otp_generated_time
        return 0

    @property
    def timeout_formated(self) -> str:
        minutes, seconds = divmod(self.timeout, 60)
        if self.valid:
            return f"{minutes} minutes, {seconds} seconds"
        return 0

    def verify(self, otp: int):
        if self.valid and otp == self.otp:
            self.verified = otp == self.otp
            return self.verified

    def generate(self) -> int:
        random.seed(get_timestamp())
        self.otp = random.randint(100_000, 999_999)

        self.modified()
        self.last_otp_generated_time = self.modified_timestamp

        run_on_thread(self.revoke_otp)
        return self.otp

    def revoke_otp(self):
        while self.alive and self.otp and not self.verified:
            if get_timestamp() - self.last_otp_generated_time >= OTP_TIMEOUT:
                self.otp = 0
                LOGGER.info(f"{self.user}: OTP revoked")


class ResetOTP(OTP):
    def __init__(self, user: User):
        OTP.__init__(self, user)
        self.verified = False

    @modifier
    def send_otp(self):
        if not self.otp:
            sent = GmailSend.send_reset_otp(
                self.user.email,
                self.user.full_name,
                self.generate(),
            )
            LOGGER.info(f"{self.user}: RESET OTP generated :: {sent}")
            return sent

    def verify(self, otp: int):
        return otp == self.otp

    def reset(self, password: str, otp: int) -> bool:
        if self.verify(otp):
            self.user.password = hash_bcrypt(password)
            self.user.save()
            return True
