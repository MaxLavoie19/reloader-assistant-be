from datetime import timedelta, datetime
from secrets import token_urlsafe

from session.repository.CredentialRepository import CredentialRepository

EMAIL_KEY = "email"
EXPIRATION_KEY = "expiration"


class SessionRepository:
    def __init__(self, credential_repository: CredentialRepository):
        self.credential_repository = credential_repository
        self.active_sessions = {}

    def authenticate(self, email: str, password: str) -> str:
        if self.credential_repository.authenticate_user(email, password):
            authentication_token = token_urlsafe(128)
            while authentication_token in self.active_sessions:
                authentication_token = token_urlsafe(128)
            self.active_sessions[authentication_token] = {
                EXPIRATION_KEY: datetime.now() + timedelta(days=1), EMAIL_KEY: email
            }
            return authentication_token
        return ''

    def logout(self, token: str):
        if token in self.active_sessions:
            self.active_sessions.__delitem__(token)

    def is_authenticated(self, token: str):
        if token not in self.active_sessions:
            return False

        now = datetime.now()
        session = self.active_sessions[token]
        expiration = session[EXPIRATION_KEY]
        is_expired = now > expiration

        if is_expired:
            self.logout(token)

        return not is_expired
