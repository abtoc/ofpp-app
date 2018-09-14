from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import Optional
from flaskr.utils.validators import WorkTime

class PerformLogFormIDM(FlaskForm):
    work_in = StringField('開始時間', validators=[Optional(), WorkTime()])
    work_out = StringField('開始時間', validators=[Optional(), WorkTime()])
    absence = BooleanField('欠席')
    absence_add = BooleanField('欠席加算')
    pickup_in = BooleanField('送迎加算（往路）')
    pickup_out = BooleanField('送迎加算（復路）')
    meal = BooleanField('食事提供加算')
    outside = BooleanField('施設外支援')
    outemp = BooleanField('施設外就労')
    visit = IntegerField('訪問支援特別加算（時間数）', validators=[Optional()])
    medical = IntegerField('医療連携体制加算', validators=[Optional()])
    experience = IntegerField('体験利用支援加算（初日ー5日目は1，6日目ー１５日目は2）', validators=[Optional()])
    remarks = StringField('備考')

class PerformLogForm(FlaskForm):
    absence = BooleanField('欠席')
    absence_add = BooleanField('欠席加算')
    pickup_in = BooleanField('送迎加算（往路）')
    pickup_out = BooleanField('送迎加算（復路）')
    meal = BooleanField('食事提供加算')
    outside = BooleanField('施設外支援')
    outemp = BooleanField('施設外就労')
    visit = IntegerField('訪問支援特別加算（時間数）', validators=[Optional()])
    medical = IntegerField('医療連携体制加算', validators=[Optional()])
    experience = IntegerField('体験利用支援加算（初日ー5日目は1，6日目ー１５日目は2）', validators=[Optional()])
    remarks = StringField('備考')
