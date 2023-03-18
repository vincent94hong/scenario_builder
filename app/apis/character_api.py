from flask import g, abort
from flask_restx import Namespace, fields, reqparse, Resource

from app.models.setting.character_model import Character as CharacterModel # , Element as ElementModel
from app.models.scenario_model import Scenario as ScenarioModel
from app.apis.func import Find


ns = Namespace(
    'users/scenarios/characters',
    description='등장인물 관련 API'
)



character = ns.model('Character', {
    'idx': fields.Integer(required=True, description='캐릭터 고유 인덱스'),
    'scenario_idx': fields.Integer(required=True, description='시나리오 고유 넘버'),
    'scenario_title': fields.String(required=True, description='시나리오 제목'),
    'name': fields.String(required=True, description='캐릭터 이름'),
    'content': fields.String(required=True, description='캐릭터 설명'),
    'created_at': fields.DateTime(description='생성일'),
    'updated_at': fields.DateTime(description='수정일'),
    'is_opened': fields.Boolean(default=False, description='공개 여부'),
    'is_deleted': fields.Boolean(default=False, description='삭제 여부'),

    'elements': fields.List(fields.Nested(ns.model('CharacterElement', {
        'element': fields.String(required=True, description='캐릭터 설정 항목'),
        'content': fields.String(required=True, description='캐릭터 설정 내용'),
        'is_opened' : fields.Boolean(default=False, description='캐릭터 설정 내용')
        })), 
        description='캐릭터 설정')
})


parser = reqparse.RequestParser()
parser.add_argument('scenario_title', required=True, help='시나리오 제목')

post_parser = parser.copy()
post_parser.add_argument('name', required=True, help='character 이름')
post_parser.add_argument('content', required=False, help='character 설명')
post_parser.add_argument('is_opened', required=False, help='character 공개 여부')

# get_parser = reqparse.RequestParser()
# get_parser.add_argument('scenario_title', required=False, help='시나리오 제목')
# get_parser.add_argument('character_name', required=True, help='character 이름')

# post_parser = reqparse.RequestParser()
# post_parser.add_argument('scenario_title', required=True, help='시나리오 제목')
# post_parser.add_argument('character_name', required=True, help='character 이름')

# post_parser.add_argument('is_opened', required=False, help='character 공개 여부')


@ns.route('')
class Character(Resource):
    @ns.expect(parser)
    @ns.marshal_list_with(character, skip_none=True)
    def get(self):
        scenario_title = parser.parse_args()['scenario_title']
        characters = CharacterModel.find_characters(scenario_title)
        return characters

    @ns.expect(post_parser)
    @ns.marshal_list_with(character, skip_none=True)
    def post(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        name = args['name']
        character = CharacterModel.find_character(scenario_title, name)
        if character:
            return abort(409)
        
        character = CharacterModel(
            scenario_idx = Find.find_scenario_idx(scenario_title).idx,
            scenario_title = scenario_title,
            name = name,
            content = args['content'],
            is_opened = args['is_opened']
        )
        g.db.add(character)
        g.db.commit()
        return character, 201

    # @ns.expect()
    # @ns.marshal_list_with(character, skip_none=True)
    # def put(self):


