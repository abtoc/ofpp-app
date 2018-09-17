from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, ValidationError
from wtforms.validators import Required, EqualTo, Optional, Email
from flaskr.models import Person, User

class UserNewForm(FlaskForm):
    userid = StringField('ログインユーザID', validators=[Required(message='必須項目です')])
    password = PasswordField('パスワード', validators=[Required(message='必須項目です')])
    confirm = PasswordField('パスワード再入力', validators=[EqualTo('password',message='パスワードが一致しません')])
    staff = BooleanField('職員')
    person_id = SelectField('対応利用者（又は対応職員）')
    email = StringField('パスワードリセット用E-Mailアドレス', validators=[Email(message='メールアドレスを入れてください'), Optional()])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.person_id.choices = [(None, '無し')] + [(ps.id, ps.name)
            for ps in Person.query.filter(Person.enabled==True).order_by(Person.name).all()
        ]
    def validate_userid(form, field):
        if len(field.data) == 0:
            return
        user = User.query.filter(User.userid == field.data).first()
        if user is not None:
            ValidationError('同一ユーザIDが指定されています')

class UserEditForm(FlaskForm):
    staff = BooleanField('職員')
    person_id = SelectField('対応利用者（又は対応職員）')
    email = StringField('パスワードリセット用E-Mailアドレス', validators=[Email(message='メールアドレスを入れてください'), Optional()])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.person_id.choices = [(None, '無し')] + [(ps.id, ps.name)
            for ps in Person.query.filter(Person.enabled==True).order_by(Person.name).all()
        ]
