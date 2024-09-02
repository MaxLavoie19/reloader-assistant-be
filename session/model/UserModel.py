from dataclasses import dataclass


@dataclass
class UserModel:
    email: str
    salt: str
    password_hash: str
    is_deactivated: bool
