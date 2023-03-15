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
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            g.user = user_id
        else:
            session.pop('user_id', None)


@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_id = form.data.get('user_id')
        user_pw = form.data.get('user_pw')
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            if security.check_password_hash(user.user_pw, user_pw):
                session['user_id'] = user_id
                return redirect(url_for('home.home'))
            else:
                return flash('not')
        else:
            return flash('not')
    # else:
    #     flash_form_error(form)

    if g.user:
        return redirect(url_for('home.home'))
    return render_template(f'{NAME}/login.html', form=form)


@bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_id = form.data.get('user_id')
        user = UserModel.find_one_by_user_id(user_id)
        if not user:
            g.db.add(
                UserModel(
                    user_id = user_id,
                    user_name = form.data.get('user_name'),
                    user_email = form.data.get('user_email'),
                    user_phone = form.data.get('user_phone'),
                    user_pw = security.generate_password_hash(form.data.get('user_pw'))
                )
            )
            g.db.commit()
            session['user_id'] = user_id
            return redirect(url_for('home.home'))
        else:
            flash('이미 존재하는 아이디입니다.')
            return redirect(request.path)
    # else:
    #     flash_form_error(form)
    return render_template(f'{NAME}/sign_up.html', form=form)


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home.home'))


def flash_form_error(form):
    for _, errors in form.errors.item():
        for e in errors:
            flash(e)