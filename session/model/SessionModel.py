from dataclasses import dataclass


@dataclass
class SessionModel:
    email: str
    expiration: str
