from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField, SelectField, ValidationError
from wtforms.validators import Required
from flaskr.models import Person
from flaskr.services.timerules import TimeRuleService

class PersonForm(FlaskForm):
    enabled = BooleanField('有効化', default='checked')
    person_id = HiddenField('id')
    name = StringField('名前', validators=[Required(message='必須項目です')])
    display = StringField('表示名')
    idm = StringField('IDM')
    timerule_id = SelectField('タイムテーブル', render_kw={'class': 'form-control'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'obj' in kwargs:
            self.person_id.data = kwargs['obj'].id
        self.timerule_id.choices = [(tr.id, tr.caption) for tr in TimeRuleService.get_all()]      
    def validate_idm(form, field):
        if len(field.data) == 0:
            return
        check = Person.query.filter_by(idm == field.data, id != form.person_id.data).first()
        if check:
            raise ValidationError('同一IDMが指定されいています')
    