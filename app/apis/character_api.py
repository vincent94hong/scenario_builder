from flask import g, abort
from flask_restx import Namespace, fields, reqparse, Resource

from app.models.setting.character_model import Character as CharacterModel # , Element as ElementModel
from app.models.scenario_model import Scenario as ScenarioModel
from app.apis.api_func import Func, CharacterFunc, ElementFunc


ns = Namespace(
    'characters',
    description='등장인물 관련 API'
)


element = ns.model('Element', {
    'element': fields.String(required=True, description='캐릭터 설정 항목'),
    'content': fields.String(required=True, description='캐릭터 설정 내용'),
    'is_opened' : fields.Boolean(default=False, description='캐릭터 설정 내용'),
})


character = ns.model('Character', {
    'idx': fields.Integer(required=True, description='캐릭터 고유 인덱스'),
    'scenario_idx': fields.Integer(required=True, description='시나리오 고유 넘버'),
    'name': fields.String(required=True, description='캐릭터 이름'),
    'content': fields.String(required=True, description='캐릭터 설명'),
    'created_at': fields.DateTime(description='생성일'),
    'updated_at': fields.DateTime(description='수정일'),
    'is_opened': fields.Boolean(default=False, description='공개 여부'),
    'is_deleted': fields.Boolean(default=False, description='삭제 여부'),

    'elements': fields.List(fields.Nested(element), description='연결된 캐릭터 설정 항목들'),
})


parser = reqparse.RequestParser()
parser.add_argument('scenario_title', required=False, help='시나리오 제목')
parser.add_argument('character_name', required=False, help='character 이름')
parser.add_argument('is_opened', required=False, help='character 공개 여부')

get_parser = reqparse.RequestParser()
get_parser.add_argument('scenario_title', required=False, help='시나리오 제목')
get_parser.add_argument('character_name', required=True, help='character 이름')

post_parser = reqparse.RequestParser()
post_parser.add_argument('scenario_title', required=True, help='시나리오 제목')
post_parser.add_argument('character_name', required=True, help='character 이름')
post_parser.add_argument('content', required=True, help='character 설명')
post_parser.add_argument('is_opened', required=False, help='character 공개 여부')


@ns.route('/admin')
class CharacterList(Resource):
    @ns.expect(parser)
    @ns.marshal_list_with(character, skip_none=True)
    def get(self):
        '''관리자 캐릭터 조회'''
        Func.admin_check()
        args = parser.parse_args()
        if args['scenario_title']:
            if args['is_opened']:
                return CharacterFunc.find_opened_characters(args)
            if args['character_name']:
                return CharacterFunc.find_character_by_name(args)
            return CharacterFunc.find_characters(args)
        if args['character_name']:
            return Character.query.filter_by(name=args['name'])
        return CharacterModel.query.all()
    

@ns.route('')
class Character(Resource):
    @ns.expect(get_parser)
    @ns.marshal_list_with(character, skip_none=True)
    def get(self):
        args = get_parser.parse_args()
        if args['scenario_title']:
            CharacterFunc.find_character_by_name(args)
        return CharacterModel.query.filter_by(name=args['character_name']).all()

    @ns.expect(post_parser)
    @ns.marshal_list_with(character, skip_none=True)
    def post(self):
        args = post_parser.parse_args()
        character = CharacterFunc.find_character_by_name(args)
        if character:
            return abort(409)
        character = CharacterModel(
            scenario_idx = ScenarioModel.find_scenario_by_title(
                g.user.idx, 
                args['scenario_title']
            ).idx,
            name = args['character_name'],
            content = args['content']
        )
        if args['is_opened']:
            character.is_opened = args['is_opened']
        g.db.add(character)
        g.db.commit()
        return character, 201

    # @ns.expect()
    # @ns.marshal_list_with(character, skip_none=True)
    # def put(self):
