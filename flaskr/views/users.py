from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flaskr import db
from flaskr.models import User
from flaskr.forms.users import UserNewForm

bp = Blueprint('users', __name__, url_prefix="/users")

@bp.route('/')
def index():
    items = User.query.order_by(User.userid).all()
    return render_template('users/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = UserNewForm()
    if form.validate_on_submit():
        try:
            user = User()
            form.populate_obj(user)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('ユーザを追加しました', 'success')
            return redirect(url_for('users.index'))
        except Exception as e:
            db.session.rollback()
            flash('ユーザ追加時にエラーが発生しました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc())
    return render_template('users/edit.pug', form=form)

@bp.route('/<id>/destroy')
def destroy(id):
    user = User.query.filter(User.id == id).first()
    if user is None:
        abort(404)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('ユーザを削除しました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('ユーザ削除時にエラーが発生しました', 'danger')
        from traceback import format_exc
        print(format_exc())
    return redirect(url_for('users.index'))
