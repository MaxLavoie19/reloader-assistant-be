import json
import sys
from typing import Callable

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.datastructures.headers import Headers

from reload.model.BrassModel import BrassModel
from reload.model.BulletModel import BulletModel
from reload.model.CaliberModel import CaliberModel
from reload.model.ChamberingModel import ChamberingModel
from reload.model.ManufacturerModel import ManufacturerModel
from reload.model.PowderModel import PowderModel
from reload.model.PrimerModel import PrimerModel
from reload.repository.ComponentRepository import ComponentRepository
from server_io.service.FileService import FileService
from session.model.UserModel import UserModel
from session.repository.CredentialRepository import CredentialRepository
from session.repository.SessionRepository import SessionRepository
from server_io.service.SerializerService.JsonSerializerService import \
    JsonSerializerService
from session.service.CryptographicHashService.BlowfishHashService import BlowfishHashService

POST = 'POST'
GET = 'GET'

app = Flask('__name__')
CORS(app)

json_file_service = FileService()
serializer_service = JsonSerializerService(json_file_service)
blowfish_hash_service = BlowfishHashService()
credential_repository = CredentialRepository(
    serializer_service=serializer_service,
    cryptographic_hash_service=blowfish_hash_service
)
session_repository = SessionRepository(credential_repository, serializer_service)

component_repository = ComponentRepository(serializer_service)


def get_token(headers: Headers):
    authorization = headers.get('Authorization', '')
    token = authorization.split("Bearer ")
    if len(token):
        return token[-1]


def authenticate(funct: Callable):
    def authenticated(*args, **kwargs):
        token = get_token(request.headers)
        if token is None:
            return "No valid auth token found", 401
        is_authenticated = session_repository.is_authenticated(token)
        if not is_authenticated:
            return "No valid auth token found", 401
        user = session_repository.get_user(token)
        return funct(token, user, *args, **kwargs)

    authenticated.__name__ = funct.__name__
    return authenticated


@app.route("/login", methods=[POST])
def login():
    data = json.loads(request.data)
    username = data.get('username', '')
    password = data.get('password', '')
    token = session_repository.authenticate(username, password)
    if token is None:
        return 'Invalid username and password combination', 400
    return jsonify(token=token)


@app.route("/logout", methods=[POST])
@authenticate
def logout(token: str, _user: UserModel):
    session_repository.logout(token)


@app.route("/ping", methods=[GET])
def ping():
    return "Pong"


@app.route("/recipes", methods=[GET])
@authenticate
def get_user_recipes(_token: str, user: UserModel):
    recipes = serializer_service.get_recipes(user.email)
    return jsonify(items=recipes)


@app.route("/chamberings", methods=[GET])
def get_chamberings():
    chambering_dicts = component_repository.get_component_list("chamberings")
    chamberings = []
    for chambering_dict in chambering_dicts:
        chamberings.append(ChamberingModel(**chambering_dict))
    return jsonify(items=chamberings)


@app.route("/brasses", methods=[GET])
def get_brasses():
    brass_dicts = component_repository.get_component_list("brasses")
    brasses = []
    for brass_dict in brass_dicts:
        brasses.append(BrassModel(**brass_dict))
    return jsonify(items=brasses)


@app.route("/bullets", methods=[GET])
def get_bullets():
    bullet_dicts = component_repository.get_component_list("bullets")
    bullets = []
    for bullet_dict in bullet_dicts:
        bullets.append(BulletModel(**bullet_dict))
    return jsonify(items=bullets)


@app.route("/calibers", methods=[GET])
def get_calibers():
    caliber_dicts = component_repository.get_component_list("calibers")
    calibers = []
    for caliber_dict in caliber_dicts:
        calibers.append(CaliberModel(**caliber_dict))
    return jsonify(items=calibers)


@app.route("/manufacturers", methods=[GET])
def get_manufacturer():
    manufacturer_dicts = component_repository.get_component_list("manufacturers")
    manufacturers = []
    for manufacturer_dict in manufacturer_dicts:
        manufacturers.append(ManufacturerModel(**manufacturer_dict))
    return jsonify(items=manufacturers)


@app.route("/powders", methods=[GET])
def get_powders():
    powder_dicts = component_repository.get_component_list("powders")
    powders = []
    for powder_dict in powder_dicts:
        powders.append(PowderModel(**powder_dict))
    return jsonify(items=powders)


@app.route("/primers", methods=[GET])
def get_primers():
    primer_dicts = component_repository.get_component_list("primers")
    primers = []
    for primer_dict in primer_dicts:
        primers.append(PrimerModel(**primer_dict))
    return jsonify(items=primers)


@app.route("/recipe", methods=[POST])
def post_user_recipe():
    # Add all inexisting sub types (brass, bullet, powder, primer, etc....)
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
