from server_io.service.FileService import FileService
from session.repository.CredentialRepository import CredentialRepository
from server_io.service.SerializerService.JsonSerializerService import \
    JsonSerializerService
from session.service.CryptographicHashService.BlowfishHashService import BlowfishHashService

json_file_service = FileService()
serializer_service = JsonSerializerService(json_file_service)
blowfish_hash_service = BlowfishHashService()
credential_repository = CredentialRepository(
    serializer_service=serializer_service,
    cryptographic_hash_service=blowfish_hash_service
)

NEW_USERNAME = "maxlavoie1960@hotmail.com"
NEW_USER_PASSWORD = "Balcam001!"

credential_repository.create_user(NEW_USERNAME, NEW_USER_PASSWORD)
