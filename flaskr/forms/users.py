from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import Required, EqualTo
from flaskr.models import User

class UserNewForm(FlaskForm):
    userid = StringField('ログインユーザID', validators=[Required(message='必須項目です')])
    password = PasswordField('パスワード', validators=[Required(message='必須項目です')])
    confirm = PasswordField('パスワード再入力', validators=[EqualTo('password',message='パスワードが一致しません')])
    def validate_userid(form, field):
        if len(field.data) == 0:
            return
        user = User.query.filter(User.userid == field.data).first()
        if user is not None:
            ValidationError('同一ユーザIDが指定されています')
