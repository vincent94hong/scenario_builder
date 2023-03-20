from flask import g, abort
from flask_restx import Namespace, fields, reqparse, Resource, inputs

from app.models.setting.background_model import Background as BackgroundModel
from app.models.setting.background_model import BackgroundElement as BackgroundElementModel
from app.models.scenario_model import Scenario as ScenarioModel
# from app.apis.func import Find


ns = Namespace(
    'users/scenarios/backgrounds/elements',
    description='등장인물 속성 관련 API'
)



element = ns.model('BackgroundElement', {
    'scenario_title': fields.String(required=True, description='시나리오 제목'),
    'background_name': fields.String(required=True, description='배경 이름'),
    'name': fields.String(required=True, description='배경 설정 항목'),
    'content': fields.String(required=True, description='배경 설정 내용'),
    'is_opened' : fields.Boolean(description='배경 설정 공개 여부')
})


parser = reqparse.RequestParser()
parser.add_argument('scenario_title', required=True, help='시나리오 제목')
parser.add_argument('background_name', required=True, help='background 이름')

post_parser = parser.copy()
post_parser.add_argument('name', required=True, help='element 이름')
post_parser.add_argument('content', required=True, help='element 설명')
post_parser.add_argument('is_opened', required=False, type=inputs.boolean, help='element 공개 여부')

put_parser = post_parser.copy()
put_parser.add_argument('re_name', required=False, help='element 이름')
put_parser.add_argument('content', required=False, help='element 설명')

delete_parser = parser.copy()
delete_parser.add_argument('name', required=True, help='element 이름')


@ns.route('')
class Element(Resource):
    @ns.expect(parser)
    @ns.marshal_list_with(element, skip_none=True)
    def get(self):
        args = parser.parse_args()
        scenario_title = args['scenario_title']
        background_name = args['background_name']
        elements = BackgroundElementModel.find_elements(g.user.id, scenario_title, background_name)
        return elements

    @ns.expect(post_parser)
    @ns.marshal_list_with(element, skip_none=True)
    def post(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        background_name = args['background_name']
        name = args['name']
        element = BackgroundElementModel.find_element(
            g.user.id, 
            scenario_title, 
            background_name,
            name
        )
        if element:
            return abort(409)
        
        element = BackgroundElementModel(
            user_id=g.user.id,
            background_idx = BackgroundModel.find_background(g.user.id, scenario_title, background_name).idx,
            scenario_title = scenario_title,
            background_name = background_name,
            name = name,
            content = args['content'],
            is_opened = args['is_opened']
        )
        g.db.add(element)
        g.db.commit()
        return element, 201

    @ns.expect(put_parser)
    @ns.marshal_list_with(element, skip_none=True)
    def put(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        background_name = args['background_name']
        name = args['name']
        element = BackgroundElementModel.find_element(g.user.id, scenario_title, background_name, name)
        if not element:
            return abort(404)
        
        if args['re_name'] != element.name:
            element.name = args['re_name']
        if args['content'] != element.content:
            element.content = args['content']
        if args['is_opened'] != element.is_opened:
            element.is_opened = args['is_opened']
        g.db.commit()
        return element
    
    @ns.expect(delete_parser)
    @ns.marshal_list_with(element, skip_none=True)
    def delete(self):
        args = delete_parser.parse_args()
        element = BackgroundElementModel.find_element(
            g.user.id, 
            scenario_title=args['scenario_title'], 
            background_name=args['background_name'],
            name = args['name']
        )
        if not element:
            return abort(404)

        g.db.delete(element)
        g.db.commit()
        return '', 204
