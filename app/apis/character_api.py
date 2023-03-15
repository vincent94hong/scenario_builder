from flask import g
from flask_restx import Api, Namespace
from app.models.setting.character_model import Character as CharacterModel, Element as ElementModel
from app.models.scenario_model import Scenario as ScenarioModel


ns = Namespace(
    'characters',
    description='등장인물 관련 API'
)