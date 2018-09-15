from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import EqualTo, Required

class LoginForm(FlaskForm):
    userid = StringField('ユーザID')
    passwd = PasswordField('パスワード')

class PasswordChangeForm(FlaskForm):
    password = PasswordField('パスワード', validators=[Required(message='必須項目です')])
    confirm = PasswordField('パスワード再入力', validators=[EqualTo('password', message='パスワードが一致しません')])
