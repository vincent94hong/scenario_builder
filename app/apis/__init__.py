from flask import Blueprint, g, abort
from flask_restx import Api
from functools import wraps

from .admin_api import ns as AdminNamespace
from .user_api import ns as UserNamespace
from .character_api import ns as CharacterNamespace
from .scenario_api import ns as ScenarioNamespace

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