from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import Required

class CompanyForm(FlaskForm):
    enabled = BooleanField('有効化', default='checked')
    name = StringField('就労先企業名',validators=[Required(message='必須入力です')])
    address = StringField('所在地', validators=[Required(message='必須入力です')])
    