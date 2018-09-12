from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField, SelectField, ValidationError
from wtforms.validators import Required
from flaskr.models import Person

class PersonForm(FlaskForm):
    person_id = HiddenField('id')
    name = StringField('名前', validators=[Required(message='必須項目です')])
    display = StringField('表示名')
    idm = StringField('IDM')
    enabled = BooleanField('有効化', default='checked')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'obj' in kwargs:
            self.person_id.data = kwargs['obj'].id
    def validate_idm(form, field):
        if len(field.data) == 0:
            return
        check = Person.query.filter(Person.idm == field.data, Person.id != form.person_id.data).first()
        if check:
            raise ValidationError('同一IDMが指定されいています')
    