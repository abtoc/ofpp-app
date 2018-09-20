from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flaskr import app, db
from flaskr.forms.recipients import RecipientForm
from flaskr.models import Recipient
from flaskr.utils.roles import login_required_staff

bp = Blueprint('recipients', __name__, url_prefix='/recipients')

@bp.route('/')
@login_required_staff
def index():
    items = Recipient.query.all()
    return render_template('recipients/index.pug', items=items)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required_staff
def edit(id):
    item = Recipient.get_or_404(id)
    form = RecipientForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('受給者証の変更ができました', 'success')
            return redirect(url_for('recipients.index'))
        except Exception as e:
            db.session.rollback()
            flash('受給者証変更時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('recipients/edit.pug', item=item, form=form)

