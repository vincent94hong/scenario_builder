from flask import g, abort, session, flash
from flask_restx import Namespace, fields, reqparse, Resource
from functools import wraps
from werkzeug import security

from app.models.user_model import User as UserModel


ns = Namespace(
    'user',
    description='User API'
)


user = ns.model('User', {
    'idx': fields.Integer(required=True, description='유저 고유 인덱스'),
    'id': fields.String(required=True, description='유저 아이디'),
    'pw': fields.String(required=True, description='유저 비밀번호'),
    'name': fields.String(required=True, description='유저 이름'),
    'email': fields.String(required=False, description='유저 이메일'),
    'phone': fields.String(required=False, description='유저 전화번호'),
    'created_at': fields.DateTime(description='생성일'),
})


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, help='user id')
parser.add_argument('pw', required=True, help='user pw')
parser.add_argument('name', required=True, help='user name')
parser.add_argument('email', required=False, help='user email')
parser.add_argument('phone', required=False, help='user phone')

put_parser = reqparse.RequestParser()
put_parser.add_argument('pw', required=False, help='user pw')
put_parser.add_argument('name', required=False, help='user name')
put_parser.add_argument('email', required=False, help='user email')
put_parser.add_argument('phone', required=False, help='user phone')

login_parser = reqparse.RequestParser()
login_parser.add_argument('id', required=True, help='user id')
login_parser.add_argument('pw', required=True, help='user pw')


@ns.route('')
class UserList(Resource):

    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        '''관리자 유저 복수 조회'''
        if g.user.id != 'admin':
            return abort(403)
        return UserModel.query.all()
    
    @ns.expect(parser)
    @ns.marshal_list_with(user, skip_none=True)
    def post(self):
        '''유저 생성'''
        args = parser.parse_args()
        id = args['id']
        user = UserModel.find_one_by_user_id(id)
        if user:
            ns.abort(409)
        user = UserModel(
            id = id,
            pw = security.generate_password_hash(args['pw']),
            name = args['name'],
            email = args['email'],
            phone = args['phone'],
        )
        g.db.add(user)
        g.db.commit()
        return user, 201


@ns.route('/admin/<id>')
@ns.param('id', '유저 아이디')
class UserAdmin(Resource):

    @ns.marshal_list_with(user, skip_none=True)
    def get(self, id):
        '''관리자 유저 단수 조회'''
        if g.user.id != 'admin':
            return abort(403)
        user = UserModel.find_one_by_user_id(id)
        return user
    
    @ns.expect(put_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def put(self, id):
        '''관리자 유저 수정'''
        args = put_parser.parse_args()
        user = UserModel.find_one_by_user_id(id)
        if g.user.id != 'admin':
            ns.abort(403)
        if args['pw'] is not None:
            user.pw = security.generate_password_hash(args['pw'])
        if args['name'] is not None:
            user.name = args['name']
        if args['email'] is not None:
            user.email = args['email']
        if args['phone'] is not None:
            user.phone = args['phone']
        g.db.commit()
        return user
    

@ns.route('/mypage')
class User(Resource):

    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        '''마이페이지 조회'''
        user = UserModel.find_one_by_user_id(g.user.id)
        return user

    @ns.expect(put_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def put(self):
        '''마이페이지 수정'''
        args = put_parser.parse_args()
        user = UserModel.find_one_by_user_id(g.user.id)
        if user.id != g.user.id:
            ns.abort(403)
        if args['pw'] is not None:
            user.pw = security.generate_password_hash(args['pw'])
        if args['name'] is not None:
            user.name = args['name']
        if args['email'] is not None:
            user.email = args['email']
        if args['phone'] is not None:
            user.phone = args['phone']
        g.db.commit()
        return user
       
    @ns.marshal_list_with(user, skip_none=True)
    def delete(self):
        '''마이페이지 삭제'''
        user = UserModel.find_one_by_user_id(g.user.id)
        session.pop('user_id', None)
        g.user = None
        g.db.delete(user)
        g.db.commit()
        return '', 204
    

@ns.route('/login')
class UserLogin(Resource):

    @ns.expect(login_parser)
    @ns.marshal_list_with(user, skip_none=True)
    def get(self):
        '''유저 전환'''
        args = login_parser.parse_args()
        user = UserModel.find_one_by_user_id(args['id'])
        if user:
            if security.check_password_hash(user.pw, args['pw']):
                session['user_id'] = user.id
                g.user = user
                return user
            else:
                return flash('비밀번호를 확인해주세요.')
        return abort(409)
