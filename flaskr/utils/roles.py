from flask_login import current_user
from functools import wraps
from flaskr import lm, cache

def check_idm(person):
    if current_user.is_admin():
        return True
    return person.idm == cache.get('person.idm')

def login_required_admin(func):
    @wraps(func)
    def decoreted_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return lm.unauthorized()
        if not current_user.is_admin():
            return lm.unauthorized()
        return func(*args, **kwargs)
    return decoreted_view

def login_required_staff(func):
    @wraps(func)
    def decoreted_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return lm.unauthorized()
        if (not current_user.is_admin()) and (not current_user.is_staff()):
            return lm.unauthorized()
        return func(*args, **kwargs)
    return decoreted_view

