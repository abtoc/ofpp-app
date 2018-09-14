from flask import abort
from flaskr import db
from flaskr.services.persons import PersonService
from flaskr.models import Recipient

class RecipientService(Recipient):
    def update(self, form):
        form.populate_obj(self)
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_or_404(cls, id):
        result = cls.query.get(id)
        if result is None:
            abort(404)
        return result