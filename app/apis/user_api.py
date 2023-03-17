from flask import g, abort, session, flash
from flask_restx import Namespace, fields, reqparse, Resource
from functools import wraps
from werkzeug import security

from app.models.user_model import User as UserModel


ns = Namespace(
    'users',
    description='User API'
)


# scenario = 


user = ns.model('User', {
    'idx': fields.Integer(required=True, description='유저 고유 인덱스'),
    'id': fields.String(required=True, description='유저 아이디'),
    'pw': fields.String(required=True, description='유저 비밀번호'),
    'name': fields.String(required=True, description='유저 이름'),
    'email': fields.String(required=False, description='유저 이메일'),
    'phone': fields.String(required=False, description='유저 전화번호'),
    'created_at': fields.DateTime(description='생성일'),

    'scenarios': fields.List(fields.Nested(
        ns.model('Scenario', {
            'idx': fields.Integer(require=True, description='시나리오 고유 번호'),
            'title': fields.String(require=True, description='시나리오 제목'),
        })), 
        description='시나리오 리스트')
})


parser = reqparse.RequestParser()
parser.add_argument('pw', required=True, help='user pw')

login_parser = parser.copy()
login_parser.add_argument('id', required=True, help='user id')

put_parser = parser.copy()
put_parser.add_argument('name', required=True, help='user name')
put_parser.add_argument('email', required=False, help='user email')
put_parser.add_argument('phone', required=False, help='user phone')


@ns.route('')
class User(Resource):
    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        '''마이페이지 조회'''
        user = UserModel.find_user(g.user.id)
        return user

    @ns.expect(put_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def put(self):
        '''마이페이지 수정'''
        args = put_parser.parse_args()
        user = UserModel.find_user(g.user.id)
        user.pw = security.generate_password_hash(args['pw'])
        user.name = args['name']
        user.email = args['email']
        user.phone = args['phone']
        g.db.commit()
        return user
       
    @ns.expect(parser)
    @ns.marshal_list_with(user, skip_none=True)
    def delete(self):
        '''회원 탈퇴'''
        user = UserModel.find_user(g.user.id)
        if not security.check_password_hash(user.pw, parser.parse_args()['pw']):
            return abort(403)
        
        g.db.delete(user)
        g.db.commit()
        session.pop('user_id', None)
        g.user = None
        return '', 204
    

# 추후 없어질 기능. 지금은 테스트 용으로 사용
@ns.route('/login')
class UserLogin(Resource):

    @ns.response(403, '비밀번호가 일치하지 않습니다.')
    @ns.expect(login_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        '''유저 전환'''
        args = login_parser.parse_args()
        user = UserModel.find_user(args['id'])
        if user:
            if security.check_password_hash(user.pw, args['pw']):
                session['user_id'] = user.id
                g.user = user
                return user
            else:
                return abort(403)
        return abort(404)
