from flask import g, abort
from flask_restx import Namespace, fields, reqparse, Resource, inputs

from app.models.setting.background_model import Background as BackgroundModel
from app.models.setting.background_model import BackgroundElement as BackgroundElementModel
from app.models.scenario_model import Scenario as ScenarioModel
# from app.apis.func import Find


ns = Namespace(
    'users/scenarios/backgrounds',
    description='배경설정 관련 API'
)



background = ns.model('Background', {
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

    'elements': fields.List(fields.Nested(ns.model('BackgroundElement', {
        'name': fields.String(required=True, description='배경 설정 항목'),
        'content': fields.String(required=True, description='배경 설정 내용'),
        'is_opened' : fields.Boolean(description='배경 설정 공개 여부')
        })), 
        description='배경 설정 리스트')
})


parser = reqparse.RequestParser()
parser.add_argument('scenario_title', required=True, help='시나리오 제목')

post_parser = parser.copy()
post_parser.add_argument('name', required=True, help='background 이름')
post_parser.add_argument('content', required=False, help='background 설명')
post_parser.add_argument('is_opened', required=False, type=inputs.boolean, help='background 공개 여부')
post_parser.add_argument('elements', action='split', help='배경이 보유 중인 설정')

put_parser = post_parser.copy()
put_parser.add_argument('re_name', required=False, help='background 이름 수정')

delete_parser = parser.copy()
delete_parser.add_argument('name', required=True, help='background 이름')


@ns.route('')
class Background(Resource):
    @ns.expect(parser)
    @ns.marshal_list_with(background, skip_none=True)
    def get(self):
        scenario_title = parser.parse_args()['scenario_title']
        backgrounds = BackgroundModel.find_backgrounds(g.user.id, scenario_title)
        return backgrounds

    @ns.response(404, '보유할 속성이 존재하지 않습니다. 속성을 먼저 만들어주세요.')
    @ns.expect(post_parser)
    @ns.marshal_list_with(background, skip_none=True)
    def post(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        name = args['name']
        background = BackgroundModel.find_background(g.user.id, scenario_title, name)
        if background:
            return abort(409)
        
        background = BackgroundModel(
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
                    element = BackgroundElementModel.find_element(
                        g.user.id,
                        scenario_title,
                        name,
                        element_name
                    )
                    if not element:
                        return abort(404)
                    background.elements.append(element)
        g.db.add(background)
        g.db.commit()
        return background, 201

    @ns.expect(put_parser)
    @ns.marshal_list_with(background, skip_none=True)
    def put(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        name = args['name']
        background = BackgroundModel.find_background(g.user.id, scenario_title, name)
        if not background:
            return abort(404)
        
        if args['re_name'] != background.name:
            background.name = args['re_name']
            elements = BackgroundElementModel.find_elements(g.user.id, scenario_title, name)
            for element in elements:
                element.background_name = args['re_name']
        if args['content'] != background.content:
            background.content = args['content']
        if args['is_opened'] != background.is_opened:
            background.is_opened = args['is_opened']
        g.db.commit()
        return background
    
    @ns.expect(delete_parser)
    @ns.marshal_list_with(background, skip_none=True)
    def delete(self):
        args = delete_parser.parse_args()
        background = BackgroundModel.find_background(
            g.user.id, 
            args['scenario_title'], 
            args['name']
        )
        if not background:
            return abort(404)

        g.db.delete(background)
        g.db.commit()
        return '', 204
