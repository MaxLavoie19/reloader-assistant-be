from session.error.UserExists import UserExists
from session.model.UserModel import UserModel
from session.service.CredentialSerializerService.ICredentialSerializerService import ICredentialSerializerService
from session.service.CryptographicHashService.ICryptographicHashService import ICryptographicHashService


class CredentialRepository:
    def __init__(
        self,
        credentials_serializer_service: ICredentialSerializerService,
        cryptographic_hash_service: ICryptographicHashService
    ):
        self.credentials_serializer_service = credentials_serializer_service
        self.cryptographic_hash_service = cryptographic_hash_service

    def is_email_unique(self, email) -> bool:
        user = self.credentials_serializer_service.load(email)
        return user is None

    def create_user(self, email: str, password: str):
        if not self.is_email_unique(email):
            raise UserExists
        salt_str, password_hash = self.cryptographic_hash_service.hash(password)
        user = UserModel(email=email, salt=salt_str, password_hash=password_hash, is_deactivated=False)
        self.credentials_serializer_service.dump(user)

    def authenticate_user(self, email: str, password: str) -> bool:
        user = self.credentials_serializer_service.load(email)
        return self.cryptographic_hash_service.is_match(password, user.password_hash)

    def deactivate_user(self, email):
        user = self.credentials_serializer_service.load(email)
        user.is_deactivated = True
        self.credentials_serializer_service.dump(user)

    def reactivate_user(self, email):
        user = self.credentials_serializer_service.load(email)
        user.is_deactivated = False
        self.credentials_serializer_service.dump(user)
