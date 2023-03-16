from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session, jsonify
from app.forms.auth_form import LoginForm, SignUpForm
from app.models.user_model import User as UserModel
from werkzeug import security
from flask_jwt_extended import *


NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix=f'/{NAME}')


@bp.before_app_request
def before_app_request():
    g.user = None
    id = session.get('user_id')
    if id:
        user = UserModel.find_one_by_user_id(id)
        if user:
            g.user = user
        else:
            session.pop('user_id', None)


@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        id = form.data.get('id')
        pw = form.data.get('pw')
        user = UserModel.find_one_by_user_id(id)
        if user:
            if not security.check_password_hash(user.pw, pw):
                flash('비밀번호를 확인해주세요.')
            else:
                session['user_id'] = id
                return redirect(url_for('home.home'))
        else:
            flash('존재하지 않는 회원입니다.')
            return redirect(request.path)
    # else:
    #     flash_form_errors(form)

    if g.user:
        return redirect(url_for('home.home'))
    return render_template(f'{NAME}/login.html', form=form)


@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        id = form.data.get('id')
        user = UserModel.find_one_by_user_id(id)
        if not user:
            g.db.add(
                UserModel(
                    id = id,
                    name = form.data.get('name'),
                    email = form.data.get('email'),
                    phone = form.data.get('phone'),
                    pw = security.generate_password_hash(form.data.get('pw'))
                )
            )
            g.db.commit()
            session['user_id'] = id
            return redirect(url_for('home.home'))
        else:
            flash('이미 존재하는 아이디입니다.')
            return redirect(request.path)
    # else:
    #     flash_form_errors(form)
    return render_template(f'{NAME}/sign_up.html', form=form)


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home.home'))


def flash_form_errors(form):
    for _, errors in form.errors.item():
        for e in errors:
            flash(e)