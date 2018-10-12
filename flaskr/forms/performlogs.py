from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SelectField, HiddenField, ValidationError
from wtforms.validators import Optional
from flaskr.utils.validators import WorkTime
from flaskr.models import WorkLog, Company

def check_absence_add(form, field):
    if (field.data) and (not form.absence.data):
        raise ValidationError('欠席にチェックしてください')

class PerformLogFormIDM(FlaskForm):
    value_ = HiddenField()
    work_in = StringField('開始時間', validators=[Optional(), WorkTime()])
    work_out = StringField('終了時間', validators=[Optional(), WorkTime()])
    absence = BooleanField('欠席')
    absence_add = BooleanField('欠席加算', validators=[check_absence_add])
    pickup_in = BooleanField('送迎加算（往路）')
    pickup_out = BooleanField('送迎加算（復路）')
    meal = BooleanField('食事提供加算')
    outside = BooleanField('施設外支援')
    visit = IntegerField('訪問支援特別加算（時間数）', validators=[Optional()])
    medical = IntegerField('医療連携体制加算', validators=[Optional()])
    experience = IntegerField('体験利用支援加算（初日ー5日目は1，6日目ー１５日目は2）', validators=[Optional()])
    company_id = SelectField('施設外就労先企業')
    remarks = StringField('備考')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'obj' in kwargs:
            obj = kwargs['obj']
            worklog = WorkLog.query.get((obj.person_id, obj.yymm, obj.dd))
            if worklog is not None:
                self.value_.data = worklog.value
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
        if bool(form.work_in.data) or bool(form.work_out.data) or bool(form.value_.data):
            raise ValidationError('勤務時間が入力されているため、欠席にはできません')
    def validate_work_out(form, field):
        if not bool(form.work_in.data):
            return
        if not bool(form.work_out.data):
            return
        if form.work_in.data > form.work_out.data:
            raise ValidationError('終了時刻は開始時刻より後の時刻にしてください')

class PerformLogForm(FlaskForm):
    work_in_ = HiddenField()
    work_out_ = HiddenField()
    value_ = HiddenField()
    absence = BooleanField('欠席')
    absence_add = BooleanField('欠席加算', validators=[check_absence_add])
    pickup_in = BooleanField('送迎加算（往路）')
    pickup_out = BooleanField('送迎加算（復路）')
    meal = BooleanField('食事提供加算')
    outside = BooleanField('施設外支援')
    visit = IntegerField('訪問支援特別加算（時間数）', validators=[Optional()])
    medical = IntegerField('医療連携体制加算', validators=[Optional()])
    experience = IntegerField('体験利用支援加算（初日ー5日目は1，6日目ー１５日目は2）', validators=[Optional()])
    remarks = StringField('備考')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'obj' in kwargs:
            obj = kwargs['obj']
            self.work_in_.data = obj.work_in
            self.work_out_.data = obj.work_out
            worklog = WorkLog.query.get((obj.person_id, obj.yymm, obj.dd))
            if worklog is not None:
                self.value_.data = worklog.value
    def populate_obj(self, obj):
        super().populate_obj(obj)
        if not bool(obj.remarks):
            obj.remarks = None     
    def validate_absence(form, field):
        if not field.data:
            return
        if bool(form.work_in_.data) or bool(form.work_out_.data) or bool(form.value_.data):
            raise ValidationError('勤務時間が入力されているため、欠席にはできません')
