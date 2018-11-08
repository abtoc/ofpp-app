from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SelectField, HiddenField, ValidationError
from wtforms.validators import Optional
from flaskr.utils.validators import WorkTime
from flaskr.models import Company

class WorkLogForm(FlaskForm):
    work_in_ = HiddenField()
    work_out_ = HiddenField()
    value = DecimalField('勤務時間', validators=[Optional()])
    break_t = DecimalField('休憩時間', validators=[Optional()])
    over_t = DecimalField('残業時間', validators=[Optional()])
    late = BooleanField('遅刻')
    leave = BooleanField('早退')
    remarks = StringField('備考')
    def populate_obj(self, obj):
        super().populate_obj(obj)
        if not bool(obj.remarks):
            obj.remarks = None

class WorkLogFormStaff(FlaskForm):
    work_in = StringField('開始時間', validators=[Optional(), WorkTime()])
    work_out = StringField('終了時間', validators=[Optional(), WorkTime()])
    value = DecimalField('勤務時間', validators=[Optional()])
    break_t = DecimalField('休憩時間', validators=[Optional()])
    over_t = DecimalField('残業時間', validators=[Optional()])
    absence = BooleanField('欠勤')
    late = BooleanField('遅刻')
    leave = BooleanField('早退')
    company_id = SelectField('施設外就労先企業')    
    remarks = StringField('備考')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_id.choices = [('', '無し')] + [
            (c.id, c.name)
            for c in Company.query.filter(
                Company.enabled == True
            ).order_by(
                Company.name
            ).all()
        ]
    def populate_obj(self, obj):
        super().populate_obj(obj)
        if not bool(obj.work_in):
            obj.work_in = None
        if not bool(obj.work_out):
            obj.work_out = None
        if not bool(obj.remarks):
            obj.remarks = None
        if not bool(obj.company_id):
            obj.company_id = None
    def validate_absence(form, field):
        if not field.data:
            return
        if bool(form.work_in.data) or bool(form.work_out.data) or bool(form.value.data):
            raise ValidationError('勤務時間が設定されているため欠勤にチェックできません')
    def validate_work_out(form, field):
        if not bool(form.work_in.data):
            return
        if not bool(form.work_out.data):
            return
        if form.work_in.data > form.work_out.data:
            raise ValidationError('終了時刻は開始時刻より後の時刻にしてください')
