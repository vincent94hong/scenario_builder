from flask import Blueprint, g, abort
from flask_restx import Api
from functools import wraps

from .admin_api import ns as AdminNamespace
from .user_api import ns as UserNamespace
from .scenario_api import ns as ScenarioNamespace
from app.apis.setting.character_api import ns as CharacterNamespace
from app.apis.setting.character_elements_api import ns as CharacterElementNamespace
from app.apis.setting.background_api import ns as BackgroundNamespace
from app.apis.setting.background_elements_api import ns as BackgroundElementNamespace
from app.apis.setting.country_api import ns as CountryNamespace
from app.apis.setting.country_elements_api import ns as CountryElementNamespace
from app.apis.setting.item_api import ns as ItemNamespace
from app.apis.setting.item_elements_api import ns as ItemElementNamespace

def check_session(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if not g.user:
            abort(401)
        return func(*args, **kwargs)
    return __wrapper


bp = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)


api = Api(
    bp,
    title='Scenario Builder API',
    version='1.0',
    doc='/docs',
    decorators=[check_session],
    description='Welcome Scenario Builder API'
)



api.add_namespace(AdminNamespace)
api.add_namespace(UserNamespace)
api.add_namespace(ScenarioNamespace)
api.add_namespace(CharacterNamespace)
api.add_namespace(CharacterElementNamespace)
api.add_namespace(BackgroundNamespace)
api.add_namespace(BackgroundElementNamespace)
api.add_namespace(CountryNamespace)
api.add_namespace(CountryElementNamespace)
api.add_namespace(ItemNamespace)
api.add_namespace(ItemElementNamespace)