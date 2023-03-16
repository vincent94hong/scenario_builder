from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import EqualTo, DataRequired


class LoginForm(FlaskForm):
    id = StringField('User Id', validators=[DataRequired()])
    pw = PasswordField('User Password', validators=[DataRequired()])


class SignUpForm(LoginForm):
    name = StringField('User Name', validators=[DataRequired()])
    email = StringField('User Email')
    phone = StringField('User Phone number')
    pw = PasswordField(
        'User Password', 
        validators=[DataRequired(), EqualTo(
            're_pw', 
            message='Password must match'
        )]
    )
    re_pw = PasswordField('Confirm Password', validators=[DataRequired()])