from flask import g, abort, session, flash
from flask_restx import Namespace, reqparse, Resource
from functools import wraps
from werkzeug import security

from app.models.user_model import User as UserModel
from app.models.scenario_model import Scenario as ScenarioModel
from app.models.setting.character_model import Character as CharacterModel
from app.apis.func import Admin

# ns.model()
from app.apis.user_api import user
from app.apis.scenario_api import scenario
from app.apis.setting.character_api import character


ns = Namespace(
    'admin',
    description='Admin API'
)


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, help='user id')

put_parser = reqparse.RequestParser()
put_parser.add_argument('pw', required=True, help='user pw')
put_parser.add_argument('name', required=True, help='user name')
put_parser.add_argument('email', required=False, help='user email')
put_parser.add_argument('phone', required=False, help='user phone')

post_parser = put_parser.copy()
post_parser.add_argument('id', required=True, help='user id')


# @ns.deprecated
@ns.response(409, 'User id is already exists.')
@ns.route('/users')
class UserList(Resource):
    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        '''유저 전체 조회'''
        # Admin.admin_check()
        return UserModel.query.all()
    
    @ns.expect(post_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def post(self):
        '''유저 생성'''
        # Admin.admin_check()
        args = post_parser.parse_args()
        id = args['id']
        user = UserModel.find_user(id)
        if user:
            ns.abort(409)
        user = UserModel(
            id = id,
            pw = security.generate_password_hash(args['pw']),
            name = args['name'],
        )
        if args['email'] is not None:
            user.email = args['email']
        if args['phone'] is not None:
            user.phone = args['phone']
        
        g.db.add(user)
        g.db.commit()
        return user, 201
    
        
# @ns.deprecated
@ns.route('/<id>')
class User(Resource):
    @ns.marshal_list_with(user, skip_none=True)
    def get(self, id):
        '''유저 조회'''
        # Admin.admin_check()
        user = UserModel.find_user(id)
        return user
 
    
    @ns.expect(put_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def put(self, id):
        '''유저 수정'''
        Admin.admin_check()
        args = put_parser.parse_args()
        user = UserModel.find_user(id)
        if not user:
            return abort(404)
        user.pw = security.generate_password_hash(args['pw'])
        user.name = args['name']
        user.email = args['email']
        user.phone = args['phone']

        g.db.commit()
        return user
    

# @ns.deprecated
@ns.route('/<id>/scenarios')
class ScenarioList(Resource):
    @ns.marshal_list_with(scenario, skip_none=True)
    def get(self, id):
        '''시나리오 전체 조회'''
        # Admin.admin_check()
        return ScenarioModel.find_scenarios(id)
    
@ns.route('/<id>/<scenario>')
class ScenarioList(Resource):
    @ns.marshal_list_with(scenario, skip_none=True)
    def get(self, id, scenario):
        '''시나리오 전체 조회'''
        # Admin.admin_check()
        return ScenarioModel.find_scenario(id, scenario)
    

# @ns.deprecated
@ns.route('/<id>/<scenario>/characters')
class CharacterList(Resource):
    @ns.marshal_list_with(character, skip_none=True)
    def get(self, id, scenario):
        '''캐릭터 전체 조회'''
        # Admin.admin_check()
        # scenario = ScenarioModel.find_scenario(id, scenario)
        return CharacterModel.find_characters(id, scenario)
    
@ns.route('/<id>/<scenario>/<character>')
class CharacterList(Resource):
    @ns.marshal_list_with(character, skip_none=True)
    def get(self, id, scenario, character):
        '''캐릭터 전체 조회'''
        # Admin.admin_check()
        # scenario = ScenarioModel.find_scenario(id, scenario)
        return CharacterModel.find_character(id, scenario, character)
    
