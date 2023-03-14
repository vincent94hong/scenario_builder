from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import EqualTo, DataRequired


class LoginForm(FlaskForm):
    user_id = StringField('User Id', validators=[DataRequired()])
    user_pw = PasswordField('User Password', validators=[DataRequired()])


class RegisterForm(LoginForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    user_pw = PasswordField(
        'User Password', 
        validators=[DataRequired(), EqualTo(
            'user_re_pw', 
            message='Password must match'
        )]
    )
    user_re_pw = PasswordField('Confirm Password', validators=[DataRequired()])