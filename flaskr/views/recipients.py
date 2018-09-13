from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flaskr.forms.recipients import RecipientForm
from flaskr.services.recipients import RecipientService
from flaskr import db

bp = Blueprint('recipients', __name__, url_prefix='/recipients')

@bp.route('/')
def index():
    items = RecipientService.get_all()
    for item in items:
        print(item.person)
    return render_template('recipients/index.pug', items=items)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    recipient = RecipientService.get_or_404(id)
    form = RecipientForm(obj=recipient)
    if form.validate_on_submit():
        try:
            recipient.update(form)
            flash('受給者証の変更ができました', 'success')
            return redirect(url_for('recipients.index'))
        except ValueError as e:
            db.session.rollback()
            flash(e, 'danger')
        except Exception as e:
            db.session.rollback()
            flash('受給者証変更時にエラーが発生しました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc)
    return render_template('recipients/edit.pug', item=recipient, form=form)

