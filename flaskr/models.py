from datetime import datetime
from uuid import uuid4
from flask_login import UserMixin
from flaskr import db
import pymysql
pymysql.install_as_MySQLdb

def _get_now():
    return datetime.now()

def _get_uuid():
    return str(uuid4())

# 利用者テーブル
class Person(db.Model):
    __tablename__ = 'persons'
    __table_args__ = (
        db.PrimaryKeyConstraint('id'),
        {'mysql_engine': 'InnoDB'}
    )
    id = db.Column(db.String(36), default=_get_uuid)
    name = db.Column(db.String(64), nullable=False)     # 名前
    display = db.Column(db.String(64), nullable=True)   # 表示名
    idm = db.Column(db.String(16), unique=True)         # Ferica IDM
    enabled = db.Column(db.Boolean, nullable=False)     # 有効化
    staff = db.Column(db.Boolean, nullable=False)       # 職員
    timerule_id = db.Column(db.String(36), db.ForeignKey('timerules.id')) # タイムテーブル
    create_at = db.Column(db.DateTime, default=_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)
    @property
    def display_or_name(self):
        return self.display if bool(self.display) else self.name
    @property
    def recipient(self):
        return Recipient.query.filter(Recipient.person_id == self.id).first()

# 受給者証テーブル
class Recipient(db.Model):
    __tablename__ = 'recipients'
    __table_args__ = (
        db.PrimaryKeyConstraint('person_id'),
        db.ForeignKeyConstraint(['person_id'], ['persons.id'], onupdate='CASCADE', ondelete='CASCADE'),
        {'mysql_engine': 'InnoDB'}
    )
    person_id = db.Column(db.String(36))                # 利用者ID
    number = db.Column(db.String(10), nullable=True)    # 受給者番号
    amount = db.Column(db.String(64), nullable=True)    # 契約支給量
    usestart = db.Column(db.Date, nullable=True)        # 利用開始日
    supply_in = db.Column(db.Date, nullable=True)       # 支給決定開始日
    supply_out = db.Column(db.Date, nullable=True)      # 支給決定終了日
    apply_in = db.Column(db.Date, nullable=True)        # 適用決定開始日
    apply_out = db.Column(db.Date, nullable=True)       # 適用決定終了日
    create_at = db.Column(db.DateTime, default=_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)
    @property
    def person(self):
        return Person.query.get(self.person_id)

# 実績記録表
class PerformLog(db.Model):
    __tablename__ = 'performlogs'
    __table_args__ = (
        db.PrimaryKeyConstraint('person_id', 'yymm', 'dd'),
        db.ForeignKeyConstraint(['person_id'], ['persons.id']),
        db.Index('performlogs_yymmdd', 'yymm', 'person_id', 'dd'),
        {'mysql_engine': 'InnoDB'}
    )
    person_id = db.Column(db.String(36))             # 利用者ID
    yymm = db.Column(db.String(8))                   # 年月
    dd = db.Column(db.Integer)                       # 日
    enabled = db.Column(db.Boolean)                  # 実績票出力対象はTrue
    presented = db.Column(db.Boolean)                # 月の日数-8を超えたらFalse
    absence = db.Column(db.Boolean, nullable=False)  # 欠席
    absence_add = db.Column(db.Boolean, nullable=False) # 欠席加算対象
    work_in  = db.Column(db.String(8))               # 開始時間
    work_out = db.Column(db.String(8))               # 終了時間
    pickup_in  = db.Column(db.Boolean)               # 送迎加算（往路）
    pickup_out = db.Column(db.Boolean)               # 送迎加算（復路）
    visit = db.Column(db.Integer)                    # 訪問支援特別加算（時間数）
    meal = db.Column(db.Boolean)                     # 食事提供加算
    medical = db.Column(db.Integer)                  # 医療連携体制加算
    experience = db.Column(db.Integer)               # 体験利用支援加算
    outside = db.Column(db.Boolean)                  # 施設外支援
    outemp = db.Column(db.Boolean)                   # 施設外就労
    remarks = db.Column(db.String(128))              # 備考
    create_at = db.Column(db.DateTime, default=_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)

# 欠席時対応加算記録
class AbsenceLog(db.Model):
    __tablename__ = 'absencelogs'
    __table_args__ = (
        db.PrimaryKeyConstraint('person_id', 'yymm', 'dd'),
        db.ForeignKeyConstraint(['person_id', 'yymm','dd'], ['performlogs.person_id','performlogs.yymm','performlogs.dd'],onupdate='CASCADE', ondelete='CASCADE'),
        db.ForeignKeyConstraint(['person_id'], ['persons.id']),
        db.ForeignKeyConstraint(['staff_id'], ['persons.id']),
        db.Index('absencelogs_yymmdd', 'yymm', 'dd'),
        {'mysql_engine': 'InnoDB'}
    )
    person_id = db.Column(db.String(36))             # 利用者ID
    yymm = db.Column(db.String(8))                   # 年月
    dd = db.Column(db.Integer)                       # 日
    enabled = db.Column(db.Boolean)                  # 月に４回以上であればFalse
    deleted = db.Column(db.Boolean)                  # 欠席加算のチェックオフになったらTrue
    contact = db.Column(db.Date)                     # 連絡日
    staff_id = db.Column(db.String(36))              # 対応職員
    reason = db.Column(db.String(128))               # 欠席理由
    remarks = db.Column(db.String(128))              # 相談援助
    create_at = db.Column(db.DateTime, default=_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)

# 勤怠記録表
class WorkLog(db.Model):
    __tablename__ = 'worklogs'
    __table_args__ = (
        db.PrimaryKeyConstraint('person_id', 'yymm', 'dd'),
        db.ForeignKeyConstraint(['person_id'], ['persons.id']),
        db.Index('worklogs_yymmdd', 'yymm', 'person_id', 'dd'),
        {'mysql_engine': 'InnoDB'}
    )
    person_id = db.Column(db.String(36))             # 利用者ID
    yymm = db.Column(db.String(8))                   # 年月
    dd = db.Column(db.Integer)                       # 日
    presented = db.Column(db.Boolean)                # 勤怠として有効ならtrue 
    work_in  = db.Column(db.String(8))               # 開始時間
    work_out = db.Column(db.String(8))               # 終了時間
    value = db.Column(db.Float)                      # 勤務時間
    break_t = db.Column(db.Float)                    # 休憩時間
    over_t = db.Column(db.Float)                     # 残業時間
    absence = db.Column(db.Boolean)                  # 欠勤
    late = db.Column(db.Boolean)                     # 遅刻
    leave = db.Column(db.Boolean)                    # 早退
    remarks = db.Column(db.String(128))              # 備考
    create_at = db.Column(db.DateTime, default=_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)

# ユーザ
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=_get_uuid)
    userid = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(128))
    create_at = db.Column(db.DateTime, default=_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)
    def set_password(self, password):
        if password:
            password = password.strip()
        self.password = generate_password_hash(password)
    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

# 時間ルールテーブル
class TimeRule(db.Model):
    __tablename__ = 'timerules'
    __table_args__ = (
        db.PrimaryKeyConstraint('id'),
        {'mysql_engine': 'InnoDB'}
    )
    id = db.Column(db.String(36), default=_get_uuid)
    caption = db.Column(db.String(64), nullable=False)  # 名前
    rules = db.Column(db.Text)                          # ルール(JSON)
    create_at = db.Column(db.DateTime, default=_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)

# オプション
class Option(db.Model):
    __tablename__ = 'options'
    __table_args__ = (
        db.PrimaryKeyConstraint('id'),
        {'mysql_engine': 'InnoDB'}
    )
    id = db.Column(db.String(36), default=_get_uuid)
    name = db.Column(db.String(64), nullable=False, unique=True)
    value = db.Column(db.String(512), nullable=False)
    create_at = db.Column(db.DateTime, default=_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)
