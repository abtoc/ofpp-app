from flaskr import db
from flaskr.models import Option

class OptionService(Option):
    @classmethod
    def get(cls, name, value=None):
        opt = cls.query.filter(cls.name == name).first()
        return opt.value if bool(opt) else value
    @classmethod
    def set(cls, name, value):
        opt = cls.query.filter(cls.name == name).first()
        if opt is None:
            opt = Option(name=name)
        opt.value = value
        db.session.add(opt) 
      
