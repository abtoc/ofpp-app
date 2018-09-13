from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flaskr.forms.persons import PersonForm
from flaskr.services.persons import PersonService
from flaskr import db
from flaskr.models import Recipient

bp = Blueprint('staffs', __name__, url_prefix='/staffs')

@bp.route('/')
def index():
    items = PersonService.get_all_staff()
    return render_template('staffs/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = PersonForm()
    if form.validate_on_submit():
        person = PersonService(staff=True)
        try:
            person.insert(form)
            flash('職員の登録ができました', 'success')
            return redirect(url_for('staffs.index'))
        except ValueError as e:
            db.session.rollback()
            flash(e, 'danger')
        except Exception as e:
            db.session.rollback()
            flash('職員登録時にエラーが発生しました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc())
    return render_template('staffs/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    person = PersonService.get_or_404(id)
    form = PersonForm(obj=person)
    if form.validate_on_submit():
        try:
            person.update(form)
            flash('職員の変更ができました', 'success')
            return redirect(url_for('staffs.index'))
        except ValueError as e:
            db.session.rollback()
            flash(e, 'danger')
        except Exception as e:
            db.session.rollback()
            flash('職員変更時にエラーが発生しました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc())
    return render_template('staffs/edit.pug', id=id, form=form)

@bp.route('/<id>/destroy')
def destroy(id):
    person = PersonService.get_or_404(id)
    try:
        person.delete()
        flash('職員の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('職員削除時にエラーが発生しました {}'.format(e), 'danger')
        from traceback import format_exc
        print(format_exc())
    return redirect(url_for('staffs.index'))
