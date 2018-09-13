from flask import abort
from flaskr import db
from flaskr.models import TimeRule

class TimeRuleService(TimeRule):
    def update(self, form):
        form.populate_obj(self)
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()
    @classmethod
    def get_or_404(cls, id):
        result = cls.get(id)
        if result is None:
            abort(404)
        return result
    @classmethod
    def get_all_enabled(cls):
        return cls.query.filter(cls.enabled == True).all()

