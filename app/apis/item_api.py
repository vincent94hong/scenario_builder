from flask import g, abort
from flask_restx import Namespace, fields, reqparse, Resource, inputs

from app.models.setting.character_model import Character as CharacterModel
from app.models.setting.item_model import Item as ItemModel
from app.models.setting.item_model import ItemElement as ItemElementModel
from app.models.scenario_model import Scenario as ScenarioModel
# from app.apis.func import Find


ns = Namespace(
    'users/scenarios/items',
    description='아이템 관련 API'
)



item = ns.model('Item', {
    'idx': fields.Integer(required=True, description='배경 고유 인덱스'),
    'user_id': fields.String(required=True, description='유저 고유 번호'),
    'scenario_idx': fields.Integer(required=True, description='시나리오 고유 넘버'),
    'scenario_title': fields.String(required=True, description='시나리오 제목'),

    'name': fields.String(required=True, description='배경 이름'),
    'content': fields.String(required=True, description='배경 설명'),
    'created_at': fields.DateTime(description='생성일'),
    'updated_at': fields.DateTime(description='수정일'),
    'is_opened': fields.Boolean(description='공개 여부'),
    'is_deleted': fields.Boolean(description='삭제 여부'),

    'elements': fields.List(fields.Nested(ns.model('ItemElement', {
        'name': fields.String(required=True, description='아이템 속성 항목'),
        'content': fields.String(required=True, description='아이템 속성 내용'),
        'is_opened' : fields.Boolean(description='아이템 속성 공개 여부')
        })), 
        description='캐릭터 설정'),
    'characters': fields.List(fields.Nested(ns.model('Character', {
        'name': fields.String(required=True, description='아이템 보유 캐릭터'),
        'content': fields.String(required=True, description='아이템 보유 캐릭터 설명'),
        'is_opened' : fields.Boolean(description='아이템 보유 캐릭터 공개 여부')
        })), 
        description='아이템을 보유한 캐릭터 리스트'),
})


parser = reqparse.RequestParser()
parser.add_argument('scenario_title', required=True, help='시나리오 제목')

post_parser = parser.copy()
post_parser.add_argument('name', required=True, help='item 이름')
post_parser.add_argument('content', required=False, help='item 설명')
post_parser.add_argument('is_opened', required=False, type=inputs.boolean, help='item 공개 여부')
post_parser.add_argument('elements', action='split', help='아이템이 보유 중인 속성')
post_parser.add_argument('characters', action='split', help='아이템을 보유 중인 캐릭터')

put_parser = post_parser.copy()
put_parser.add_argument('re_name', required=False, help='item 이름 수정')

delete_parser = parser.copy()
delete_parser.add_argument('name', required=True, help='item 이름')


@ns.route('')
class Item(Resource):
    @ns.expect(parser)
    @ns.marshal_list_with(item, skip_none=True)
    def get(self):
        scenario_title = parser.parse_args()['scenario_title']
        items = ItemModel.find_items(g.user.id, scenario_title)
        return items

    @ns.response(404, '보유할 속성/캐릭터가 존재하지 않습니다. 속성/캐릭터를 먼저 만들어주세요.')
    @ns.expect(post_parser)
    @ns.marshal_list_with(item, skip_none=True)
    def post(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        name = args['name']
        item = ItemModel.find_item(g.user.id, scenario_title, name)
        if item:
            return abort(409)
        
        item = ItemModel(
            user_id=g.user.id,
            scenario_idx = ScenarioModel.find_scenario(g.user.id, scenario_title).idx,
            scenario_title = scenario_title,
            name = name,
            content = args['content'],
            is_opened = args['is_opened']
        )
        elements = args['elements']
        if elements:
            for element_name in elements:
                if element_name:
                    element = ItemElementModel.find_element(
                        g.user.id,
                        scenario_title,
                        name,
                        element_name
                    )
                    if not element:
                        return abort(404)
                    item.elements.append(element)
        characters = args['characters']
        if characters:
            for character_name in characters:
                if character_name:
                    character = CharacterModel.find_character(
                        g.user.id,
                        scenario_title,
                        character_name
                    )
                    if not character:
                        return abort(404)
                    item.characters.append(character)
        g.db.add(item)
        g.db.commit()
        return item, 201

    @ns.expect(put_parser)
    @ns.marshal_list_with(item, skip_none=True)
    def put(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        name = args['name']
        item = ItemModel.find_item(g.user.id, scenario_title, name)
        if not item:
            return abort(404)
        
        if args['re_name'] != item.name:
            item.name = args['re_name']
            elements = ItemElementModel.find_elements(g.user.id, scenario_title, name)
            for element in elements:
                element.item_name = args['re_name']
        if args['content'] != item.content:
            item.content = args['content']
        if args['is_opened'] != item.is_opened:
            item.is_opened = args['is_opened']
        g.db.commit()
        return item
    
    @ns.expect(delete_parser)
    @ns.marshal_list_with(item, skip_none=True)
    def delete(self):
        args = delete_parser.parse_args()
        item = ItemModel.find_item(
            g.user.id, 
            args['scenario_title'], 
            args['name']
        )
        if not item:
            return abort(404)

        g.db.delete(item)
        g.db.commit()
        return '', 204
