from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flaskr.forms.persons import PersonForm
from flaskr.services.persons import PersonService
from flaskr import db
from flaskr.models import Recipient

bp = Blueprint('persons', __name__, url_prefix='/persons')

@bp.route('/')
def index():
    items = PersonService.get_all_no_staff()
    return render_template('persons/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = PersonForm()
    if form.validate_on_submit():
        person = PersonService()
        person.populate_form(form)
        try:
            person.validate()
            person.staff = False
            person.recipient = Recipient()
            db.session.add(person)
            db.session.commit()
            flash('利用者の登録ができました', 'success')
            return redirect(url_for('persons.index'))
        except ValueError as e:
            db.session.rollback()
            flash(e, 'danger')
        except Exception as e:
            db.session.rollback()
            flash('利用者登録時にエラーが発生しました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc())
    return render_template('persons/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    person = PersonService.get_or_404(id)
    form = PersonForm(obj=person)
    if form.validate_on_submit():
        person.populate_form(form)
        try:
            person.validate()
            db.session.add(person)
            db.session.commit()
            flash('利用者の変更ができました', 'success')
            return redirect(url_for('persons.index'))
        except ValueError as e:
            db.session.rollback()
            flash(e, 'danger')
        except Exception as e:
            db.session.rollback()
            flash('利用者変更時にエラーが発生しました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc())
    return render_template('persons/edit.pug', id=id, form=form)

@bp.route('/<id>/destroy')
def destroy(id):
    person = PersonService.get_or_404(id)
    db.session.delete(person)
    try:
        db.session.commit()
        flash('利用者の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('利用者削除時にエラーが発生しました {}'.format(e), 'danger')
        from traceback import format_exc
        print(format_exc())
    return redirect(url_for('persons.index'))
