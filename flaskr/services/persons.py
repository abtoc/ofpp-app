from flask import abort
from flaskr import db
from flaskr.models import Person

class PersonService(Person):
    def populate_form(self,form):
        form.populate_obj(self)
        if not bool(self.display):
            self.display = None
        if not bool(self.idm):
            self.idm = None
    def validate(self):
        pass
    @classmethod
    def get(cls, id):
        return cls.query.filter(cls.id == id).first()
    @classmethod
    def get_or_404(cls, id):
        result = cls.get(id)
        if result is None:
            abort(404)
        return result
    def get_idm(cls, idm):
        return cls.query.filter(cls.idm == idm).first()
    @classmethod
    def get_all_enabled(cls):
        return cls.query.filter(cls.enabled == True).all()
    @classmethod
    def get_all_staff(cls):
        return cls.query.filter(cls.staff == True).all()
    @classmethod
    def get_all_no_staff(cls):
        return cls.query.filter(cls.staff != True).all()
