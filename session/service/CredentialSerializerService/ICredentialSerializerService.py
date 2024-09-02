from typing import Union

from session.model.UserModel import UserModel


class ICredentialSerializerService:
    def load(self, email: str) -> Union[UserModel, None]:
        raise NotImplementedError()

    def dump(self, user: UserModel):
        raise NotImplementedError()
