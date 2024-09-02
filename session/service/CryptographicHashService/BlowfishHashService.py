import bcrypt

from session.service.CryptographicHashService.ICryptographicHashService import ICryptographicHashService

ENCODING = 'utf-8'


class BlowfishHashService(ICryptographicHashService):
    def hash(self, data: str) -> (str, str):
        encoded_data = data.encode(ENCODING)
        salt = bcrypt.gensalt()
        encoded_hash = bcrypt.hashpw(encoded_data, salt)
        salt_str = salt.decode(ENCODING)
        hash_str = encoded_hash.decode(ENCODING)
        return salt_str, hash_str

    def is_match(self, data: str, hash_str: str) -> bool:
        encoded_data = data.encode(ENCODING)
        encoded_hash = hash_str.encode(ENCODING)
        is_match = bcrypt.checkpw(encoded_data, encoded_hash)
        return is_match
