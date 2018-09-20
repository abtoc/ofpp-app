from flask import request, flash
from flask_login import current_user
from functools import wraps
from flaskr import lm, cache

def check_idm(person):
    #臨時対応とする
    #if current_user.is_admin():
    #    return True
    return person.idm == cache.get('person.idm')

def login_required_admin(func):
    @wraps(func)
    def decoreted_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return lm.unauthorized()
        if not current_user.is_admin():
            flash('admin権限が必要です。adminユーザでログインしてください', 'danger')
            return lm.unauthorized()
        return func(*args, **kwargs)
    return decoreted_view

def login_required_staff(func):
    @wraps(func)
    def decoreted_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return lm.unauthorized()
        if (not current_user.is_admin()) and (not current_user.is_staff()):
            flash('職員の権限が必要です。職員ユーザでログインしてください', 'danger')
            return lm.unauthorized()
        return func(*args, **kwargs)
    return decoreted_view

def login_required_person(func):
    @wraps(func)
    def decoreted_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return lm.unauthorized()
        if current_user.is_admin():
            return func(*args, **kwargs)
        if current_user.is_staff():
            return func(*args, **kwargs)
        if current_user.person_id == request.view_args.get('id'):
            return func(*args, **kwargs)
        flash('指定された利用者しか参照できません。該当利用者でログインしてください', 'danger')
        return lm.unauthorized()
    return decoreted_view
