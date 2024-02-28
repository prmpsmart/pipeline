from ..constants.config import LOGGER, SESSION_TIMEOUT
from ..utils.commons import run_on_thread
from ..services.mail.otp import OTP, ResetOTP
from ..models import *
from ..utils.base import Child, SingletonManager
from ..utils.commons import get_timestamp


class Session(Child):
    def __init__(self, user: User):
        super().__init__()

        self.user = user
        self.client = Client(self, user)
        self.session_db: SessionDb = SessionDbs.create(
            id=self.id,
            created_timestamp=self.modified_timestamp,
            user_id=self.user.id,
        )

    @property
    def valid(self) -> bool:
        return (get_timestamp() - self.modified_timestamp) <= SESSION_TIMEOUT

    def set_sid(self, sid: str):
        self.client.set_sid(sid)

    def remove_sid(self):
        self.client.remove_sid()

    def kill(self):
        self.client.kill()
        super().kill()
        self.session_db.deleted_timestamp = self.modified_timestamp
        self.session_db.save()


class Client(Child):
    def __init__(
        self,
        session: Session,
        user: User,
        fcm_token: str = "",
    ):
        super().__init__()

        self.user = user
        self.session = session
        self.otp = OTP(user)

        self.fcm_token = fcm_token
        self.sid: str = ""

    @property
    def verified(self) -> bool:
        return self.user.verified

    # @modifier
    def send_otp(self) -> bool:
        return self.otp.send_otp()

    def verify_otp(self, otp: int) -> bool:
        valid = self.otp.verify(otp)
        if valid:
            self.user.verified = True
            self.user.save()
        return valid

    def set_sid(self, sid: str):
        self.sid = sid

    def remove_sid(self):
        self.sid = None

    def kill(self):
        self.otp.kill()
        super().kill()


class Sessions(SingletonManager):
    def __init__(self):
        super().__init__()

        self.session_emails: dict[str, Session] = {}
        self.session_users_ids: dict[str, Session] = {}
        self.reset_otps: dict[str, ResetOTP] = {}

        self.clearing_reset_passwords = False
        self.started = False

        self.sids: dict[str, Session] = {}

    def set_session_sid(self, sid: str, session: Session):
        session.set_sid(sid)
        self.sids[sid] = session

    def remove_session_sid(self, sid: str) -> Session:
        if session := self.sids.get(sid):
            session.remove_sid()
            del self.sids[sid]
            return session

    def create_session(self, user: User) -> None | Session:
        session = Session(user)
        child = self.add_child(session)
        if child:
            return session

    def add_child(self, session: Session) -> bool:
        if super().add_child(session):
            self.session_emails[session.user.email] = session
            self.session_users_ids[session.user.id] = session
            return session

    def get_by_email(self, email: str) -> None | Session:
        return self.session_emails.get(email)

    def get_by_user_id(self, user_id: str) -> None | Session:
        return self.session_users_ids.get(user_id)

    def get_reset(self, email: str):
        return self.reset_otps.get(email)

    def set_reset_password(self, email: str) -> None | ResetOTP:
        user = Users.child("email", email)

        if user:
            reset_otp = ResetOTP(user)
            self.reset_otps[email] = reset_otp

            if not self.clearing_reset_passwords:
                run_on_thread(self.clear_reset_passwords)
            return reset_otp

    def reset_password(
        self,
        email: str,
        password: str,
        otp: str,
    ) -> bool:
        if email in self.reset_otps:
            rpass = self.reset_otps[email]
            if rpass.reset(password, otp):
                del self.reset_otps[email]
                return True
        return False

    def clear_reset_passwords(self):
        if self.clearing_reset_passwords:
            return

        self.clearing_reset_passwords = True

        while self.alive and self.reset_otps:
            reset_otps = list(self.reset_otps.values())
            for reset_otp in reset_otps:
                if not reset_otp.valid:
                    del self.reset_otps[reset_otp.id]

        self.clearing_reset_passwords = False

    def clear_sessions(self):
        LOGGER.info(f"Started validating {self.__class__.__name__}")

        if self.started:
            return

        while self.alive:
            sessions: list[Session] = self.values()
            for session in sessions:
                if not session.valid:
                    session.kill()
                    LOGGER.info(f"Session Timeout :: {session.client.user.email}")
                    self.remove_child(session)

        self.started = False
        LOGGER.info(f"Ended validating {self.__class__.__name__}\n")

    def kill(self):
        reset_otps = self.reset_otps.values()
        for reset_otp in reset_otps:
            reset_otp.kill()

        sessions = self.children.values()
        for session in sessions:
            session.kill()
        return super().kill()


Sessions = Sessions()
