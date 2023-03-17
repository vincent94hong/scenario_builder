from flask import g, abort, flash
from flask_restx import Api, Namespace, fields, reqparse, Resource
from app.models.scenario_model import Scenario as ScenarioModel
from app.models.user_model import User as UserModel
from app.apis.api_func import Func


ns = Namespace(
    'scenarios',
    description='시나리오 관련 API'
)


scenario = ns.model('Scenario', {
    'idx': fields.Integer(required=True, description='시나리오 고유 번호'),
    'user_idx': fields.String(required=True, description='유저 고유 번호'),
    'title': fields.String(required=True, description='시나리오 제목'),
    'content': fields.String(required=True, description='시나리오 설명'),
    'created_at': fields.DateTime(description='생성일'),
    'updated_at': fields.DateTime(description='수정일'),
})


search_user_parser = reqparse.RequestParser()
search_user_parser.add_argument('title', required=False, help='scenario title')

search_parser = search_user_parser.copy()
search_parser.add_argument('user_id', required=False, help='user id')

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('title', required=True, help='scenario title')


post_parser = reqparse.RequestParser()
post_parser.add_argument('title', required=True, help='scenario title')
post_parser.add_argument('content', required=False, help='scenario content')

put_parser = post_parser.copy()
put_parser.add_argument('re_title', required=False, help='scenario title upadate')


@ns.route('/admin')
class ScenarioList(Resource):
    @ns.expect(search_parser)
    @ns.marshal_list_with(scenario, skip_none=True)
    def get(self):
        '''시나리오 조회'''
        Func.admin_check()
        args = search_parser.parse_args()
        user = UserModel.find_user(args['user_id'])
        title = args['title']
        if user:
            if title:
                return ScenarioModel.find_scenario_by_title(user.idx, title)
            else:
                return ScenarioModel.find_scenarios_sort_user(user.idx)
        if title:
            return ScenarioModel.find_scenarios_sort_title(title)
        return ScenarioModel.query.all()
    

@ns.route('')
class UserScenario(Resource):
    @ns.expect(search_user_parser)
    @ns.marshal_list_with(scenario, skip_none=True)
    def get(self):
        '''시나리오 조회'''
        title = search_user_parser.parse_args()['title']
        if title:
            return ScenarioModel.find_scenario_by_title(g.user.idx, title)
        return ScenarioModel.find_scenarios_sort_user(g.user.idx)

    @ns.expect(post_parser)
    @ns.marshal_list_with(scenario, skip_none=True)
    def post(self):
        '''시나리오 생성'''
        args = post_parser.parse_args()
        title = args['title']
        scenario = ScenarioModel.find_scenario_by_title(g.user.idx, title)
        if scenario:
            return ns.abort(409)
        scenario = ScenarioModel(
            user_idx = g.user.idx,
            title = title,
            content = args['content'],
        )
        g.db.add(scenario)
        g.db.commit()
        return scenario, 201
    
    @ns.expect(put_parser)
    @ns.marshal_list_with(scenario, skip_none=True)
    def put(self):
        '''시나리오 수정'''
        args = put_parser.parse_args()
        title = args['title']
        scenario = ScenarioModel.find_scenario_by_title(g.user.idx, title)
        if not scenario:
            return ns.abort(409)
        if args['re_title'] is not None:
            scenario.title = args['re_title']
        if args['content'] is not None:
            scenario.content = args['content']
        g.db.commit()
        return scenario
    
    @ns.expect(delete_parser)
    @ns.marshal_list_with(scenario, skip_none=True)
    def delete(self):
        '''시나리오 삭제'''
        title = delete_parser.parse_args()['title']
        scenario = ScenarioModel.find_scenario_by_title(g.user.idx, title)
        if not scenario:
            return ns.abort(409)
        g.db.delete(scenario)
        g.db.commit()
        return '', 204
