import dataclasses
from pathlib import Path
from typing import Union

from server_io.service.JsonFileService import JsonFileService
from session.model.UserModel import UserModel
from session.service.CredentialSerializerService.ICredentialSerializerService import ICredentialSerializerService


class JsonFileCredentialSerializerService(ICredentialSerializerService):
    def __init__(self, json_file_service: JsonFileService):
        self.json_file_service = json_file_service

    @staticmethod
    def get_user_folder(email: str):
        return f"./data/users/{email}"

    def get_file_path(self, email: str):
        # TODO: refactor to be stateless.
        #   This class will be used to save recipes in data/users/<email>/recipes/<recipe_name>/recipe.json
        #   sessions in data/users/<email>/sessions/<session_id>.json
        #   public data in data/(bullets/primers,...)/<object_id>.json
        #   blocks in data/users/<email>/blocks/<block_datetime>.json
        #   and in data/users/<email>/recipes/<recipe_name>/blocks/<block_datetime>.json
        user_folder = self.get_user_folder(email)
        Path(user_folder).mkdir(parents=True, exist_ok=True)
        return f"{user_folder}/user.json"

    def load(self, email: str) -> Union[UserModel, None]:
        # TODO: this method will accept an email, file name, and data then return a dictionary
        file_path = self.get_file_path(email)
        user_dict = self.json_file_service.load(file_path)
        if user_dict is None or len(user_dict) == 0:
            return None
        user = UserModel(**user_dict)
        return user

    def dump(self, user: UserModel):
        # TODO: this method will accept an email, file name, and a dictionary then write it as a json
        file_path = self.get_file_path(user.email)
        user_dict = dataclasses.asdict(user)
        self.json_file_service.save(file_path, user_dict)
