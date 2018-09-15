from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from flaskr.forms.persons import PersonForm
from flaskr.services.persons import PersonService
from flaskr import db
from flaskr.models import Recipient

bp = Blueprint('persons', __name__, url_prefix='/persons')

@bp.route('/')
@login_required
def index():
    items = PersonService.get_all_no_staff()
    return render_template('persons/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PersonForm()
    if form.validate_on_submit():
        person = PersonService(staff=False)
        try:
            person.insert(form)
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
@login_required
def edit(id):
    person = PersonService.get_or_404(id)
    form = PersonForm(obj=person)
    if form.validate_on_submit():
        try:
            person.update(form)
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
@login_required
def destroy(id):
    person = PersonService.get_or_404(id)
    try:
        person.delete()
        flash('利用者の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('利用者削除時にエラーが発生しました {}'.format(e), 'danger')
        from traceback import format_exc
        print(format_exc())
    return redirect(url_for('persons.index'))
