from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField, SelectField, ValidationError
from wtforms.validators import Required
from flaskr.models import Person
from flaskr.models import TimeRule

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
        self.timerule_id.choices = [(tr.id, tr.caption) for tr in TimeRule.query.order_by(TimeRule.caption).all()]     
    def populate_obj(self, obj):
        super().populate_obj(obj)
        if not bool(obj.display):
            obj.display = None
        if not bool(obj.idm):
            obj.idm = None
    def validate_idm(form, field):
        if len(field.data) == 0:
            return
        check = Person.query.filter(Person.idm == field.data, id != form.person_id.data).first()
        if check:
            raise ValidationError('同一IDMが指定されいています')
           