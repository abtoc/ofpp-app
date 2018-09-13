from flask import abort
from flaskr import db
from flaskr.models import Person, Recipient

class PersonService(Person):
    def insert(self, form):
        self.update(form)
        recipient = Recipient(person_id=self.id)
        db.session.add(recipient)
        db.session.commit()
    def update(self, form):
        form.populate_obj(self)
        if not bool(self.display):
            self.display = None
        if not bool(self.idm):
            self.idm = None
        db.session.add(self)
        db.session.commit()
    def delete(self):
        if bool(self.recipient):
            db.session.delete(self.recipient)
        db.session.delete(self)
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
    @classmethod
    def get_all_no_staff_enabled(cls):
        return cls.query.filter(cls.enabled == True, cls.staff != True).all()
