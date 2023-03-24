from flask import g, abort
from flask_restx import Api, Namespace, fields, reqparse, Resource, inputs
from app.models.scenario_model import Scenario as ScenarioModel
# from app.models.user_model import User as UserModel


ns = Namespace(
    'users/scenarios',
    description='시나리오 관련 API'
)


# character = 


scenario = ns.model('Scenario', {
    # 'idx': fields.Integer(required=True, description='시나리오 고유 번호'),
    # 'user_id': fields.String(required=True, description='유저 고유 번호'),
    'title': fields.String(required=True, description='시나리오 제목'),
    'content': fields.String(required=True, description='시나리오 설명'),
    # 'created_at': fields.DateTime(description='생성일'),
    # 'updated_at': fields.DateTime(description='수정일'),

    # 'characters': fields.List(fields.Nested(
    #     ns.model('Character', {
    #         'idx': fields.Integer(require=True, description='캐릭터 고유 번호'),
    #         'name': fields.String(require=True, description='캐릭터 이름'),
    #         'is_opened': fields.Boolean(description='캐릭터 공개 여부')
    #     })), 
    #     description='캐릭터 리스트'),
    # 'backgrounds': fields.List(fields.Nested(
    #     ns.model('Background', {
    #         'idx': fields.Integer(require=True, description='설정 고유 번호'),
    #         'name': fields.String(require=True, description='설정 이름'),
    #         'is_opened': fields.Boolean(description='설정 공개 여부')
    #     })), 
    #     description='배경 설정 리스트'),
    # 'countries': fields.List(fields.Nested(
    #     ns.model('Country', {
    #         'idx': fields.Integer(require=True, description='지역/국가 고유 번호'),
    #         'name': fields.String(require=True, description='지역/국가 이름'),
    #         'is_opened': fields.Boolean(description='지역/국가 공개 여부')
    #     })), 
    #     description='지역/국가 리스트'),
    # 'items': fields.List(fields.Nested(
    #     ns.model('Item', {
    #         'idx': fields.Integer(require=True, description='아이템 고유 번호'),
    #         'name': fields.String(require=True, description='아이템 이름'),
    #         'is_opened': fields.Boolean(description='아이템 공개 여부')
    #     })), 
    #     description='아이템 리스트'),
})


search_parser = reqparse.RequestParser()
search_parser.add_argument('title', required=False, help='scenario title')

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='scenario title')

post_parser = parser.copy()
post_parser.add_argument('content', required=False, help='scenario content')
    

@ns.route('')
class Scenario(Resource):
    @ns.marshal_list_with(scenario, skip_none=True)
    def get(self):
        '''시나리오 조회'''
        return ScenarioModel.find_scenarios(g.user.id)

    @ns.response(409, 'This Scenario Title is already exists.')
    @ns.expect(post_parser)
    @ns.marshal_list_with(scenario, skip_none=True)
    def post(self):
        '''시나리오 생성'''
        args = post_parser.parse_args()
        title = args['title']
        scenario = ScenarioModel.find_scenario(g.user.id, title)
        if scenario:
            return ns.abort(409)
        scenario = ScenarioModel(
            user_id = g.user.id,
            title = title,
            content = args['content'],
        )
        g.db.add(scenario)
        g.db.commit()
        return scenario, 201
    
    @ns.response(404, '수정할 시나리오가 없습니다. 시나리오 제목을 다시 입력해주세요.')
    @ns.expect(post_parser)
    @ns.marshal_list_with(scenario, skip_none=True)
    def put(self):
        '''시나리오 수정'''
        args = post_parser.parse_args()
        scenario = ScenarioModel.find_scenario(g.user.id, args['scenario'])
        if not scenario:
            return ns.abort(404)
        scenario.title = args['title']
        scenario.content = args['content']
        g.db.commit()
        return scenario
    
    @ns.response(404, '삭제할 시나리오가 없습니다. 시나리오 제목을 다시 입력해주세요.')
    @ns.expect(parser)
    @ns.marshal_list_with(scenario, skip_none=True)
    def delete(self):
        '''시나리오 삭제'''
        args = parser.parse_args()
        scenario = ScenarioModel.find_scenario(g.user.id, args['scenario'])
        if not scenario:
            return ns.abort(404)
        g.db.delete(scenario)
        g.db.commit()
        return '', 204
    