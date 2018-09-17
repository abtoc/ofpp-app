from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from flaskr.models import Person

class AbsenseLogForm(FlaskForm):
    contact = DateField('連絡日', validators=[Required(message='必須項目です')])
    staff_id = SelectField('対応職員', render_kw={'class': 'form-control'})
    reason = StringField('欠席理由', validators=[Required(message='必須項目です')])
    remarks = StringField('相談援助', validators=[Required(message='必須項目です')])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.staff_id.choices = [
            (p.id, p.name)
            for p in Person.query.filter(Person.staff == True, Person.enabled == True).order_by(Person.name)
        ]
        obj = kwargs['obj']
        if self.contact.data is None:
            self.contact.data = obj.date
        if obj.staff_id is None:
            if current_user.person_id is not None:
                self.staff_id.data = current_user.person_id

    