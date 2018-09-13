from flaskr import db
from flaskr.services.persons import PersonService
from flaskr.models import Recipient

class RecipientService(Recipient):
    def update(self, form):
        form.populate_obj(self)
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.person_id == id).first()
    @classmethod
    def get_or_404(cls, id):
        result = cls.get(id)
        if result is None:
            abort(404)
        return result
    @classmethod
    def get_all(cls):
        return cls.query.all()
    @classmethod
    def get_all_enabled():
        persons = PersonService.get_all_no_staff_enabled()
        return [person.recipient for person in persons]
