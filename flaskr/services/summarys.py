from sqlalchemy import func
from flaskr import db
from flaskr.models import Person, PerformLog, WorkLog

class SummaryService:
    def __init__(self, id, yymm):
        self.id = id
        self.yymm = yymm
        # 利用日数
        q = db.session.query(
           func.count(PerformLog.presented)
        ).filter(
            PerformLog.person_id == self.id,
            PerformLog.yymm == yymm,
            PerformLog.presented == True
        ).first()
        self.usedate = q[0]
        # 勤務日数
        q = db.session.query(
            func.count(WorkLog.presented)
        ).filter(
            WorkLog.person_id == self.id,
            WorkLog.yymm == yymm,
            WorkLog.presented == True
        ).first()
        self.presented = q[0]
        # 勤務時間
        q = db.session.query(
            func.sum(WorkLog.value)
        ).filter(
            WorkLog.person_id == self.id,
            WorkLog.yymm == yymm,
            WorkLog.presented == True
        ).first()
        self.value = q[0]
        # 欠勤
        q = db.session.query(
            func.count(WorkLog.absence)
        ).filter(
            WorkLog.person_id == self.id,
            WorkLog.yymm == yymm,
            WorkLog.absence == True
        ).first()
        self.absence = q[0]
        # 遅刻
        q = db.session.query(
            func.count(WorkLog.late)
        ).filter(
            WorkLog.person_id == self.id,
            WorkLog.yymm == yymm,
            WorkLog.late == True
        ).first()
        self.late = q[0]
        # 早退
        q = db.session.query(
            func.count(WorkLog.leave)
        ).filter(
            WorkLog.person_id == self.id,
            WorkLog.yymm == yymm,
            WorkLog.leave == True
        ).first()
        self.leave = q[0]
    @property
    def person(self):
        return Person.get(self.id)
    @classmethod
    def get_all(cls, yymm):
        persons = Person.query.filter(
            Person.staff == False,
            Person.enabled == True
        ).order_by(
            Person.name
        ).all()
        items = []
        for person in persons:
            items.append(SummaryService(person.id, yymm))
        return items

