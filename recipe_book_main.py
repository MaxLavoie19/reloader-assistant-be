import json
import sys
from typing import Callable

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.datastructures.headers import Headers

from reload.mapper.BrassMapper import brass_to_dict_mapper
from reload.mapper.BulletMapper import bullet_to_dict_mapper
from reload.mapper.ChamberingMapper import chambering_to_dict_mapper
from reload.mapper.PowderMapper import powder_to_dict_mapper
from reload.mapper.PrimerMapper import primer_to_dict_mapper
from reload.model.BrassModel import BrassModel
from reload.model.BulletModel import BulletModel
from reload.model.CaliberModel import CaliberModel
from reload.model.ChamberingModel import ChamberingModel
from reload.model.ManufacturerModel import ManufacturerModel
from reload.model.PowderModel import PowderModel
from reload.model.PrimerModel import PrimerModel
from reload.model.RecipeModel import RecipeModel
from reload.repository.ComponentRepository import ComponentRepository
from reload.repository.RecipeRepository import RecipeRepository
from server_io.service.FileService import FileService
from session.model.UserModel import UserModel
from session.repository.CredentialRepository import CredentialRepository
from session.repository.SessionRepository import SessionRepository
from server_io.service.SerializerService.JsonSerializerService import \
    JsonSerializerService
from session.service.CryptographicHashService.BlowfishHashService import BlowfishHashService

POST = 'POST'
GET = 'GET'
BRASS_KEY = "brass"
BULLET_KEY = "bullet"
PRIMER_KEY = "primer"
POWDER_KEY = "powder"
CHAMBERING_KEY = "chambering"
CALIBER_KEY = "caliber"
MANUFACTURER_KEY = "manufacturer"

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
recipe_repository = RecipeRepository(serializer_service)

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
            print("No token in header", file=sys.stderr)
            return "No valid auth token found", 401
        is_authenticated = session_repository.is_authenticated(token)
        if not is_authenticated:
            print("No token isn't active", file=sys.stderr)
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
@authenticate
def post_user_recipe(_token: str, user: UserModel):
    data = json.loads(request.data)
    brass_dict = data.get(BRASS_KEY)
    chambering_dict = brass_dict.get(CHAMBERING_KEY)
    brass_manufacturer_dict = brass_dict.get(MANUFACTURER_KEY)
    caliber_dict = chambering_dict.get(CALIBER_KEY)
    brass_manufacturer = ManufacturerModel(**brass_manufacturer_dict)
    caliber = CaliberModel(**caliber_dict)
    chambering = ChamberingModel(**{**chambering_dict, 'caliber': caliber})
    brass = BrassModel(**{**brass_dict, 'manufacturer': brass_manufacturer, 'chambering': chambering})

    bullet_dict = data.get(BULLET_KEY)
    bullet_manufacturer_dict = bullet_dict.get(MANUFACTURER_KEY)
    bullet_manufacturer = ManufacturerModel(**bullet_manufacturer_dict)
    bullet = BulletModel(
        id=bullet_dict.get('id', ''),
        caliber=caliber,
        model=bullet_dict.get('model', ''),
        weight_in_grains=bullet_dict.get('weightInGrains', ''),
        g1_ballistic_coefficient=bullet_dict.get('g1BallisticCoefficient', ''),
        g7_ballistic_coefficient=bullet_dict.get('g7BallisticCoefficient', ''),
        sectional_density=bullet_dict.get('sectionalDensity', ''),
        manufacturer=bullet_manufacturer
    )

    primer_dict = data.get(PRIMER_KEY)
    primer_manufacturer_dict = primer_dict.get(MANUFACTURER_KEY)
    primer_manufacturer = ManufacturerModel(**primer_manufacturer_dict)
    primer = PrimerModel(**{**primer_dict, 'manufacturer': primer_manufacturer})

    powder_dict = data.get(POWDER_KEY)
    powder_manufacturer_dict = powder_dict.get(MANUFACTURER_KEY)
    powder_manufacturer = ManufacturerModel(**powder_manufacturer_dict)
    powder = PowderModel(**{**powder_dict, 'manufacturer': powder_manufacturer})

    recipe = RecipeModel(
        id=data['id'],
        name=data['name'],
        bullet_seating_depth=data.get('bulletSeatingDepth', ''),
        min_powder_quantity_grains=data.get('minPowderQuantityGrains', ''),
        max_powder_quantity_grains=data.get('maxPowderQuantityGrains', ''),
        cartridge_overall_length_mm=data.get('cartridgeOverallLengthMm', ''),
        cartridge_base_to_ogive_mm=data.get('cartridgeBaseToOgiveMm', ''),
        brass=brass,
        bullet=bullet,
        primer=primer,
        powder=powder,
        notes=data['notes']
    )

    component_repository.get_or_create_component('calibers', caliber.__dict__, id_key='name')
    component_repository.get_or_create_component('chamberings', chambering_to_dict_mapper(chambering))
    component_repository.get_or_create_component('manufacturers', brass_manufacturer.__dict__, id_key='name')
    component_repository.get_or_create_component('manufacturers', bullet_manufacturer.__dict__, id_key='name')
    component_repository.get_or_create_component('manufacturers', primer_manufacturer.__dict__, id_key='name')
    component_repository.get_or_create_component('manufacturers', powder_manufacturer.__dict__, id_key='name')
    component_repository.get_or_create_component('brasses', brass_to_dict_mapper(brass))
    component_repository.get_or_create_component('bullets', bullet_to_dict_mapper(bullet))
    component_repository.get_or_create_component('primers', primer_to_dict_mapper(primer))
    component_repository.get_or_create_component('powders', powder_to_dict_mapper(powder))
    recipe_repository.save_recipe(user.email, recipe)
    return 'Ok', 200


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
