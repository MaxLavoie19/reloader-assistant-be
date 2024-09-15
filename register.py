from server_io.service.JsonFileService import JsonFileService
from session.repository.CredentialRepository import CredentialRepository
from session.service.CredentialSerializerService.JsonFileCredentialSerializerService import \
    JsonFileCredentialSerializerService
from session.service.CryptographicHashService.BlowfishHashService import BlowfishHashService

json_file_service = JsonFileService()
json_file_credential_serializer_service = JsonFileCredentialSerializerService(json_file_service)
blowfish_hash_service = BlowfishHashService()
credential_repository = CredentialRepository(
    credentials_serializer_service=json_file_credential_serializer_service,
    cryptographic_hash_service=blowfish_hash_service
)

NEW_USERNAME = "maxlavoie1960@hotmail.com"
NEW_USER_PASSWORD = "Balcam001!"

credential_repository.create_user(NEW_USERNAME, NEW_USER_PASSWORD)
