from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from flaskr import app, db
from flaskr.forms.persons import PersonForm
from flaskr.models import Person, Recipient

bp = Blueprint('staffs', __name__, url_prefix='/staffs')

@bp.route('/')
@login_required
def index():
    items = Person.query.filter(
        Person.staff == True
    ).order_by(
        Person.name
    ).all()
    return render_template('staffs/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PersonForm()
    if form.validate_on_submit():
        item = Person(staff=True)
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('職員の登録ができました', 'success')
            return redirect(url_for('staffs.index'))
        except Exception as e:
            db.session.rollback()
            flash('職員登録時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('staffs/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = Person.get(id)
    form = PersonForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        try:
            db.session.commit()
            flash('職員の変更ができました', 'success')
            return redirect(url_for('staffs.index'))
        except Exception as e:
            db.session.rollback()
            flash('職員変更時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('staffs/edit.pug', id=id, form=form)

@bp.route('/<id>/destroy')
@login_required
def destroy(id):
    item = Person.get(id)
    db.session.delete(item)
    try:
        db.session.commit()
        flash('職員の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('職員削除時にエラーが発生しました {}'.format(e), 'danger')
        app.logger.exception(e)       
    return redirect(url_for('staffs.index'))
