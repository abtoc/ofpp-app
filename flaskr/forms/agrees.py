from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from flaskr.models import Company

class AgreeForm(FlaskForm):
    caption = StringField('名前', validators=[Required(message='必須項目です')])
    company_id = SelectField('就業先企業名')
    agree_in = DateField('契約開始日')
    agree_out = DateField('契約終了日')
    content = TextAreaField('作業内容', render_kw={'rows': 3}, validators=[Required(message='必須項目です')]) 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_id.choices = [
            (c.id, c.name)
            for c in Company.query.filter(
                Company.enabled == True
            ).order_by(
                Company.name
            ).all()
        ]