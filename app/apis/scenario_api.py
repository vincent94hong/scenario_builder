from flask import g
from flask_restx import Api, Namespace, fields, reqparse, Resource
# from app.models.setting.character_model import Character as CharacterModel # , Element as ElementModel
from app.models.scenario_model import Scenario as ScenarioModel


ns = Namespace(
    'scenarios',
    description='시나리오 관련 API'
)


character = ns.model('Character', {
    'name' : fields.String(required=True, description='캐릭터 이름'),
    'content' : fields.String(required=True, description='캐릭터 설명'),
})


scenario = ns.model('Scenario', {
    'idx' : fields.Integer(required=True, description='시나리오 고유 인덱스'),
    'title' : fields.String(required=True, description='시나리오 제목'),
    'content' : fields.String(required=True, description='시나리오 설명'),
    'characters' : fields.List(fields.Nested(character), description='연결된 캐릭터들'),

    'created_at' : fields.DateTime(description='생성일'),
    'updated_at' : fields.DateTime(description='수정일'),
    'is_deleted' : fields.Boolean(description='삭제 여부'),
})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='scenario title')
# parser.add_argument('only_name', required=False, help='charactetitler get type')
# parser.add_argument('is_opened', required=False, help='character 공개 여부')


@ns.route('')
class ScenarioList(Resource):
    @ns.marshal_list_with(scenario, skip_none=True)
    @ns.expect(parser)
    def get(self):
        args = parser.parse_args()

        scenario_model = ScenarioModel.find_one_by_scenario_title(args['scenario_title'])
        # scenario_characters = CharacterModel.find_all_characters_by_scenario_title(args['scenario_title'])
        return scenario_model # , scenario_characters
