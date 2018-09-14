from flask import abort
from flaskr import db
from flaskr.models import AbsenceLog

class AbsenceLogService(AbsenceLog):
    def update(self, form):
        form.populate_obj(self)
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_or_new(cls, id, yymm, dd):
        result = cls.query.get((id, yymm, dd))
        if result is None:
            result = cls(person_id=id, yymm=yymm, dd=dd)
        return result
    @classmethod
    def get_or_404(cls, id, yymm, dd):
        result = cls.query.get((id, yymm, dd))
        if result is None:
            abort(404)
        return result
    @classmethod
    def get_date(cls, id, d):
        yymm = d.strftime('%Y%m')
        dd = d.day
        return cls.query.get(id, yymm, dd)
