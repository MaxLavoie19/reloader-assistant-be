from flask import Flask, request


from server_io.service.JsonFileService import JsonFileService
from session.repository.CredentialRepository import CredentialRepository
from session.repository.SessionRepository import SessionRepository
from session.service.CredentialSerializerService.JsonFileCredentialSerializerService import \
    JsonFileCredentialSerializerService
from session.service.CryptographicHashService.BlowfishHashService import BlowfishHashService

POST = 'POST'
GET = 'GET'

app = Flask('__name__')

json_file_service = JsonFileService()
json_file_credential_serializer_service = JsonFileCredentialSerializerService(json_file_service)
blowfish_hash_service = BlowfishHashService()
credential_repository = CredentialRepository(
    credentials_serializer_service=json_file_credential_serializer_service,
    cryptographic_hash_service=blowfish_hash_service
)
session_repository = SessionRepository(credential_repository)


@app.route("/login", methods=[POST])
def login():
    print('request.values', request.values)
    print('request.args', request.args)
    print('request.data', request.data)
    print('request.authorization', request.authorization)


@app.route("/logout", methods=[POST])
def logout():
    print('request.values', request.values)
    print('request.args', request.args)
    print('request.data', request.data)
    print('request.authorization', request.authorization)


@app.route("/logout", methods=[POST])
def register():
    pass


@app.route("/recipes", methods=[GET])
def get_user_recipes():
    pass


@app.route("/recipe", methods=[POST])
def post_user_recipe():
    # Add all inexisting sub types (brass, bullet, powder, primer, etc....)
    pass


@app.route("/brasses", methods=[GET])
def get_brasses():
    pass


@app.route("/bullets", methods=[GET])
def get_bullets():
    pass


@app.route("/calibers", methods=[GET])
def get_calibers():
    pass


@app.route("/chambers", methods=[GET])
def get_chambers():
    pass


@app.route("/manufacturer", methods=[GET])
def get_manufacturer():
    pass


@app.route("/powders", methods=[GET])
def get_powders():
    pass


@app.route("/primers", methods=[GET])
def get_primers():
    pass

# TODO: prebuilt recipes (hornady match, etc...)
# TODO: std over dates
# TODO: std over session time (1st magasine, 2nd magasine, etc...)
# TODO: recipe avg & std speed, accuracy,
# TODO: recipes avg & std speed, accuracy per grains of powder (x: grains, y: accuracy std, or x: grains, y: avg speed, or x: grains, y: std speed)
# TODO: adjusted recipes' block accuracy  (compensate for the std over session, std over dates, etc...)
# TODO: log drop over distance
# TODO: ballistic calculator 2.0
#   effective bc
#   estimate drop over distance and time of flight
#   produce zero tables (distance: clicks)
#       clicks per x yards
#       every x inch of drop
