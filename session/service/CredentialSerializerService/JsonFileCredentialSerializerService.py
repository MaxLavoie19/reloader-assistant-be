import dataclasses
from typing import Union

from server_io.service.JsonFileService import JsonFileService
from session.model.UserModel import UserModel
from session.service.CredentialSerializerService.ICredentialSerializerService import ICredentialSerializerService


class JsonFileCredentialSerializerService(ICredentialSerializerService):
    def __init__(self, json_file_service: JsonFileService):
        self.json_file_service = json_file_service

    @staticmethod
    def get_file_path(email: str):
        return f"./users/{email}.json"

    def load(self, email: str) -> Union[UserModel, None]:
        file_path = self.get_file_path(email)
        user_dict = self.json_file_service.load(file_path)
        if len(user_dict) == 0:
            return None
        user = UserModel(**user_dict)
        return user

    def dump(self, user: UserModel):
        file_path = self.get_file_path(user.email)
        user_dict = dataclasses.asdict(user)
        self.json_file_service.save(file_path, user_dict)
