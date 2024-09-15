import dataclasses
from datetime import timedelta, datetime
from secrets import token_urlsafe
from typing import Dict

from server_io.service.SerializerService.JsonSerializerService import JsonSerializerService
from session.model.SessionModel import SessionModel
from session.repository.CredentialRepository import CredentialRepository


class SessionRepository:
    def __init__(self, credential_repository: CredentialRepository, serializer_service: JsonSerializerService):
        self.credential_repository = credential_repository
        self.active_sessions: Dict[str, SessionModel] = {}
        self.serializer_service = serializer_service

    def register(self, email: str, password: str) -> bool:
        is_unique = self.credential_repository.is_email_unique(email)
        if not is_unique:
            return False
        self.credential_repository.create_user(email, password)
        return True

    def authenticate(self, email: str, password: str) -> str:
        if self.credential_repository.authenticate_user(email, password):
            authentication_token = token_urlsafe(128)
            while authentication_token in self.active_sessions:
                authentication_token = token_urlsafe(128)
            self.active_sessions[authentication_token] = SessionModel(
                email=email,
                expiration=(datetime.now() + timedelta(days=1)).isoformat(),
            )
            active_session_dict = {}
            for token, active_session in self.active_sessions.items():
                active_session_dict[token] = dataclasses.asdict(active_session)
            self.serializer_service.dump_sessions(active_session_dict)
            return authentication_token

    def logout(self, token: str):
        if token in self.active_sessions:
            self.active_sessions.__delitem__(token)

    def get_user(self, token: str):
        session = self.active_sessions[token]
        email = session.email
        user = self.credential_repository.get_user(email)
        return user

    def is_authenticated(self, token: str):
        if token not in self.active_sessions:
            return False

        now = datetime.now()
        session = self.active_sessions[token]
        expiration = datetime.fromisoformat(session.expiration)
        is_expired = now > expiration

        if is_expired:
            self.logout(token)

        return not is_expired
