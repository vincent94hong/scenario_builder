from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.auth_form import LoginForm, RegisterForm
from app.models.user_model import User as UserModel
from app import db

NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix=f'/{NAME}')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     user_id = form.data.get('user_id')
    #     user_pw = form.data.get('user_pw')
        # user = UserModel.find_one_by_user_id(user_id)
        # if user:
        #     if user.user_pw != user_pw:
        #         flash('Password is not vaild.')
        # else: flash('User Id is not exists.')

    return render_template(f'{NAME}/login.html', form=form)


@bp.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        user_name = form.data.get('user_name')
        user_pw = form.data.get('user_pw')
        user = UserModel.find_one_by_user_id(user_id)
        if not user:
            db.session.add(
                UserModel(
                    user_id = user_id,
                    user_name = user_name,
                    user_pw = user_pw
                )
            )
            db.session.commit()
    return render_template(f'{NAME}/register.html', form=form)


@bp.route('/logout')
def logout():
    return redirect(url_for('home.home'))