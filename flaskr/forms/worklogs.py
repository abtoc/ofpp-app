from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, HiddenField, ValidationError
from wtforms.validators import Optional
from flaskr.utils.validators import WorkTime

class WorkLogForm(FlaskForm):
    work_in_ = HiddenField()
    work_out_ = HiddenField()
    value = DecimalField('勤務時間', validators=[Optional()])
    break_t = DecimalField('休憩時間', validators=[Optional()])
    over_t = DecimalField('残業時間', validators=[Optional()])
    late = BooleanField('遅刻')
    leave = BooleanField('早退')
    remarks = StringField('備考')

class WorkLogFormStaff(FlaskForm):
    work_in = StringField('開始時間', validators=[Optional(), WorkTime()])
    work_out = StringField('終了時間', validators=[Optional(), WorkTime()])
    value = DecimalField('勤務時間', validators=[Optional()])
    break_t = DecimalField('休憩時間', validators=[Optional()])
    over_t = DecimalField('残業時間', validators=[Optional()])
    absence = BooleanField('欠勤')
    late = BooleanField('遅刻')
    leave = BooleanField('早退')
    remarks = StringField('備考')
    def validate_absence(form, field):
        if not field.data:
            return
        if bool(form.work_in) or bool(form.work_out) or bool(form.value):
            raise ValidationError('勤務時間が設定されているため欠勤にチェックできません')
