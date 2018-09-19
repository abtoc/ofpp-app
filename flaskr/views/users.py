from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required,current_user
from flaskr import app, db
from flaskr.models import User
from flaskr.forms.users import UserNewForm, UserEditForm
from flaskr.utils.roles import login_required_admin

bp = Blueprint('users', __name__, url_prefix="/users")

@bp.route('/')
@login_required_admin
def index():
    items = User.query.order_by(User.userid).all()
    return render_template('users/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required_admin
def create():
    form = UserNewForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('ユーザを追加しました', 'success')
            return redirect(url_for('users.index'))
        except Exception as e:
            db.session.rollback()
            flash('ユーザ追加時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('users/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required_admin
def edit(id):
    user = User.get_or_404(id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        try:
            db.session.commit()
            flash('ユーザを更新しました', 'success')
            return redirect(url_for('users.index'))
        except Exception as e:
            db.session.rollback()
            flash('ユーザ追加時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    kw = dict(
        id = id,
        userid = user.userid,
        form=form
    )
    return render_template('users/edit.pug', **kw)


@bp.route('/<id>/destroy')
@login_required_admin
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
        app.logger.exception(e)
    return redirect(url_for('users.index'))
