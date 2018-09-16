from datetime import date
from dateutil.relativedelta import relativedelta
from flask import abort
from flaskr import db
from flaskr.services.persons import PersonService
from flaskr.models import Recipient

class RecipientService(Recipient):
    def update(self, form):
        form.populate_obj(self)
        db.session.add(self)
        db.session.commit()
    def is_supply_over(self):
        if not bool(self.supply_out):
            return False
        dead = date.today()
        dead += relativedelta(months=1)
        return self.supply_out < dead     
    def is_apply_over(self):
        if not bool(self.apply_out):
            return False
        dead = date.today()
        dead += relativedelta(months=1)
        return self.apply_out < dead     
    @classmethod
    def get_or_404(cls, id):
        result = cls.query.get(id)
        if result is None:
            abort(404)
        return result