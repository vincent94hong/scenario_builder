# from flask import g
# from flask_restx import Api, Namespace, fields, reqparse, Resource
# from app.models.setting.character_model import Character as CharacterModel # , Element as ElementModel
# # from app.models.scenario_model import Scenario as ScenarioModel


# ns = Namespace(
#     'characters',
#     description='등장인물 관련 API'
# )


# element = ns.model('Element', {
#     'content_name': fields.String(required=True, description='캐릭터 설정 항목'),
#     'content': fields.String(required=True, description='캐릭터 설정 내용'),
# })


# character = ns.model('Character', {
#     'idx': fields.Integer(required=True, description='캐릭터 고유 인덱스'),
#     'user_id': fields.String(required=True, description='유저 아이디'),
#     'scenario_title': fields.String(required=True, description='시나리오 제목'),
#     'name': fields.String(required=True, description='캐릭터 이름'),
#     'content': fields.String(required=True, description='캐릭터 설명'),

#     'elements': fields.List(fields.Nested(element), description='연결된 캐릭터 설정 항목들'),

#     'created_at': fields.DateTime(description='생성일'),
#     'updated_at': fields.DateTime(description='수정일'),
#     'is_opened': fields.Boolean(description='공개 여부'),
#     'is_deleted': fields.Boolean(description='삭제 여부'),
# })


# parser = reqparse.RequestParser()
# parser.add_argument('name', required=True, help='character name')
# # parser.add_argument('only_name', required=False, help='character get type')
# parser.add_argument('is_opened', required=False, help='character 공개 여부')
# parser.add_argument('scenario_title', required=True, help='시나리오 제목')


# @ns.route('')
# class CharacterList(Resource):
#     @ns.marshal_list_with(character, skip_none=True)
#     @ns.expect(parser)
#     def get(self):
#         args = parser.parse_args()

#         characters = CharacterModel.query.all() # find_one_by_character_name(args['name'])
#         return characters