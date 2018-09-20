from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flaskr.forms.persons import PersonForm
from flaskr import app, db
from flaskr.models import Person, Recipient
from flaskr.utils.roles import login_required_staff

bp = Blueprint('persons', __name__, url_prefix='/persons')

@bp.route('/')
@login_required_staff
def index():
    items = Person.query.filter(
        Person.staff == False
    ).order_by(
        Person.name
    ).all()
    return render_template('persons/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required_staff
def create():
    form = PersonForm()
    if form.validate_on_submit():
        item = Person(staff=False)
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            recipient = Recipient(person_id=item.id)
            db.session.add(recipient)
            db.session.commit()
            flash('利用者の登録ができました', 'success')
            return redirect(url_for('persons.index'))
        except Exception as e:
            db.session.rollback()
            flash('利用者登録時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('persons/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required_staff
def edit(id):
    item = Person.get_or_404(id)
    form = PersonForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('利用者の変更ができました', 'success')
            return redirect(url_for('persons.index'))
        except Exception as e:
            db.session.rollback()
            flash('利用者変更時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('persons/edit.pug', id=id, form=form)

@bp.route('/<id>/destroy')
@login_required_staff
def destroy(id):
    item = Person.get_or_404(id)
    if bool(item.recipient):
        db.session.delete(item.recipient)
    db.session.delete(item)
    try:
        db.session.commit()
        flash('利用者の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('利用者削除時にエラーが発生しました {}'.format(e), 'danger')
        app.logger.exception(e)
    return redirect(url_for('persons.index'))
