from flask import g, abort
from flask_restx import Namespace, fields, reqparse, Resource, inputs

from app.models.setting.character_model import Character as CharacterModel
from app.models.setting.character_model import CharacterElement as CharacterElementModel
from app.models.setting.item_model import Item as ItemModel
from app.models.scenario_model import Scenario as ScenarioModel
# from app.apis.func import Find


ns = Namespace(
    'users/scenarios/characters',
    description='등장인물 관련 API'
)



character = ns.model('Character', {
    'idx': fields.Integer(required=True, description='캐릭터 고유 인덱스'),
    'user_id': fields.String(required=True, description='유저 고유 번호'),
    'scenario_idx': fields.Integer(required=True, description='시나리오 고유 넘버'),
    'scenario_title': fields.String(required=True, description='시나리오 제목'),

    'name': fields.String(required=True, description='캐릭터 이름'),
    'content': fields.String(required=True, description='캐릭터 설명'),
    'created_at': fields.DateTime(description='생성일'),
    'updated_at': fields.DateTime(description='수정일'),
    'is_opened': fields.Boolean(description='공개 여부'),
    'is_deleted': fields.Boolean(description='삭제 여부'),

    'elements': fields.List(fields.Nested(ns.model('CharacterElement', {
        'name': fields.String(required=True, description='캐릭터 설정 항목'),
        'content': fields.String(required=True, description='캐릭터 설정 내용'),
        'is_opened' : fields.Boolean(description='캐릭터 설정 내용')
        })), 
        description='캐릭터 설정'),
    'items': fields.List(fields.Nested(ns.model('Item', {
        'name': fields.String(required=True, description='아이템 항목'),
        'content': fields.String(required=False, description='아이템 내용'),
        'is_opened' : fields.Boolean(description='캐릭터 보유 아이템')
        })), 
        description='캐릭터의 보유 아이템 리스트'),
})


parser = reqparse.RequestParser()
parser.add_argument('scenario_title', required=True, help='시나리오 제목')

post_parser = parser.copy()
post_parser.add_argument('name', required=True, help='character 이름')
post_parser.add_argument('content', required=False, help='character 설명')
post_parser.add_argument('is_opened', required=False, type=inputs.boolean, help='character 공개 여부')
post_parser.add_argument('elements', action='split', help='캐릭터가 보유 중인 속성')
post_parser.add_argument('items', action='split', help='character 소유 아이템')

put_parser = post_parser.copy()
put_parser.add_argument('re_name', required=False, help='character 이름 수정')

delete_parser = parser.copy()
delete_parser.add_argument('name', required=True, help='character 이름')


@ns.route('')
class Character(Resource):
    @ns.expect(parser)
    @ns.marshal_list_with(character, skip_none=True)
    def get(self):
        scenario_title = parser.parse_args()['scenario_title']
        characters = CharacterModel.find_characters(g.user.id, scenario_title)
        return characters

    @ns.response(404, '보유할 속성/아이템이 존재하지 않습니다. 속성/아이템을 먼저 만들어주세요.')
    @ns.expect(post_parser)
    @ns.marshal_list_with(character, skip_none=True)
    def post(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        name = args['name']
        character = CharacterModel.find_character(g.user.id, scenario_title, name)
        if character:
            return abort(409)
        
        character = CharacterModel(
            user_id=g.user.id,
            scenario_idx = ScenarioModel.find_scenario(g.user.id, scenario_title).idx,
            scenario_title = scenario_title,
            name = name,
            content = args['content'],
            is_opened = args['is_opened'],
        )
        elements = args['elements']
        if elements:
            for element_name in elements:
                if element_name:
                    element = CharacterElementModel.find_element(
                        g.user.id,
                        scenario_title,
                        name,
                        element_name
                    )
                    if not element:
                        return abort(404)
                    character.elements.append(element)
        items = args['items']
        if items:
            for item_name in items:
                if item_name:
                    item = ItemModel.find_item(
                        g.user.id,
                        scenario_title,
                        item_name
                    )
                    if not item:
                        return abort(404)
                    character.items.append(item)
        g.db.add(character)
        g.db.commit()
        return character, 201

    @ns.expect(put_parser)
    @ns.marshal_list_with(character, skip_none=True)
    def put(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        name = args['name']
        character = CharacterModel.find_character(g.user.id, scenario_title, name)
        if not character:
            return abort(404)
        
        if args['re_name'] != character.name:
            character.name = args['re_name']
            elements = CharacterElementModel.find_elements(g.user.id, scenario_title, name)
            for element in elements:
                element.character_name = args['re_name']
        if args['content'] != character.content:
            character.content = args['content']
        if args['is_opened'] != character.is_opened:
            character.is_opened = args['is_opened']
        g.db.commit()
        return character
    
    @ns.expect(delete_parser)
    @ns.marshal_list_with(character, skip_none=True)
    def delete(self):
        args = delete_parser.parse_args()
        character = CharacterModel.find_character(
            g.user.id, 
            args['scenario_title'], 
            args['name']
        )
        if not character:
            return abort(404)

        g.db.delete(character)
        g.db.commit()
        return '', 204
