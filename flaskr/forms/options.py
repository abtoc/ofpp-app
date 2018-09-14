from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Required, Regexp

class OptionForm(FlaskForm):
    office_number = StringField('事業所番号', validators=[Regexp(message='数字10桁で入力してください', regex='^[0-9]{10}$')])
    office_name = StringField('事業所名', validators=[Required(message='必須項目です')])
