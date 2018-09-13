from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Optional

class RecipientForm(FlaskForm):
    number = StringField('受給者番号', validators=[Required(message='入力必須です')])
    amount = StringField('契約支給量', validators=[Required(message='入力必須です')])
    usestart = DateField('利用開始日', validators=[Optional()])
    supply_in = DateField('支給開始日', validators=[Optional()])
    supply_out = DateField('支給終了日', validators=[Optional()])
    apply_in = DateField('適用開始日', validators=[Optional()])
    apply_out = DateField('適用終了日', validators=[Optional()])
    def validate_supply_out(form, field):
        if (field.data is None) or (form.supply_in.data is None):
            return
        if form.supply_in.data > field.data:
            raise ValidationError('支給終了日は開始日より先の日付を入力してください')
    def validate_apply_out(form, field):
        if (field.data is None) or (form.apply_in.data is None):
            return
        if form.apply_in.data > field.data:
            raise ValidationError('適用終了日は開始日より先の日付を入力してください')