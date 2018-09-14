from flaskr import db
from flaskr.models import AbsenceLog

class AbsenceLogService(AbsenceLog):
    @classmethod
    def get(cls, id, yymm, dd):
        return cls.query.filter(cls.person_id==id, cls.yymm==yymm, cls.dd==dd).first()
    @classmethod
    def get_or_new(cls, id, yymm, dd):
        result = cls.get(id, yymm, dd)
        if result is None:
            result = cls(person_id=id, yymm=yymm, dd=dd)
        return result
    @classmethod
    def get_date(cls, id, d):
        yymm = d.strftime('%Y%m')
        dd = d.day
        return get(id, yymm, dd)
