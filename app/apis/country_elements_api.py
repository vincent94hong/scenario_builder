from flask import g, abort
from flask_restx import Namespace, fields, reqparse, Resource, inputs

from app.models.setting.country_model import Country as CountryModel
from app.models.setting.country_model import CountryElement as CountryElementModel
from app.models.scenario_model import Scenario as ScenarioModel
# from app.apis.func import Find


ns = Namespace(
    'users/scenarios/countrys/elements',
    description='지역/국가 관련 API'
)



element = ns.model('CountryElement', {
    'scenario_title': fields.String(required=True, description='시나리오 제목'),
    'country_name': fields.String(required=True, description='지역/국가 이름'),
    'name': fields.String(required=True, description='지역/국가 하위 지역'),
    'content': fields.String(required=True, description='지역/국가 하위 지역 내용'),
    'is_opened' : fields.Boolean(description='지역/국가 하위 지역 공개 여부')
})


parser = reqparse.RequestParser()
parser.add_argument('scenario_title', required=True, help='시나리오 제목')
parser.add_argument('country_name', required=True, help='country 이름')

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
        country_name = args['country_name']
        elements = CountryElementModel.find_elements(g.user.id, scenario_title, country_name)
        return elements

    @ns.expect(post_parser)
    @ns.marshal_list_with(element, skip_none=True)
    def post(self):
        args = post_parser.parse_args()
        scenario_title = args['scenario_title']
        country_name = args['country_name']
        name = args['name']
        element = CountryElementModel.find_element(
            g.user.id, 
            scenario_title, 
            country_name,
            name
        )
        if element:
            return abort(409)
        
        element = CountryElementModel(
            user_id=g.user.id,
            country_idx = CountryModel.find_country(g.user.id, scenario_title, country_name).idx,
            scenario_title = scenario_title,
            country_name = country_name,
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
        country_name = args['country_name']
        name = args['name']
        element = CountryElementModel.find_element(g.user.id, scenario_title, country_name, name)
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
        element = CountryElementModel.find_element(
            g.user.id, 
            scenario_title=args['scenario_title'], 
            country_name=args['country_name'],
            name = args['name']
        )
        if not element:
            return abort(404)

        g.db.delete(element)
        g.db.commit()
        return '', 204
