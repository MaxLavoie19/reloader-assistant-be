from session.error.UserExists import UserExists
from session.model.UserModel import UserModel
from server_io.service.SerializerService.JsonSerializerService import JsonSerializerService
from session.service.CryptographicHashService.ICryptographicHashService import ICryptographicHashService


class CredentialRepository:
    def __init__(
        self,
        serializer_service: JsonSerializerService,
        cryptographic_hash_service: ICryptographicHashService
    ):
        self.serializer_service = serializer_service
        self.cryptographic_hash_service = cryptographic_hash_service

    def is_email_unique(self, email) -> bool:
        user_dict = self.serializer_service.load_user(email)
        return user_dict is None

    def get_user(self, email: str) -> UserModel:
        user_dict = self.serializer_service.load_user(email)
        user = UserModel(**user_dict)
        return user

    def create_user(self, email: str, password: str):
        if not self.is_email_unique(email):
            raise UserExists
        salt_str, password_hash = self.cryptographic_hash_service.hash(password)
        user = UserModel(email=email, salt=salt_str, password_hash=password_hash, is_deactivated=False)
        self.serializer_service.dump_user(user)

    def authenticate_user(self, email: str, password: str) -> bool:
        user = self.get_user(email)
        if user is None:
            return False
        return self.cryptographic_hash_service.is_match(password, user.password_hash)

    def deactivate_user(self, email):
        user = self.get_user(email)
        user.is_deactivated = True
        self.serializer_service.dump_user(user)

    def reactivate_user(self, email):
        user = self.get_user(email)
        user.is_deactivated = False
        self.serializer_service.dump_user(user)
