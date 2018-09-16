from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from flaskr.forms.options import OptionForm
from flaskr.models import Option
from flaskr import db

bp = Blueprint('options', __name__, url_prefix='/options')

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = OptionForm()
    if form.validate_on_submit():
        Option.set('office_number', form.office_number.data)
        Option.set('office_name', form.office_name.data)
        try:
            db.session.commit()
            flash('設定を反映しました','success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('設定反映時にエラーが出ました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc)
    elif request.method == 'GET':
        form.office_number.data = Option.get('office_number')
        form.office_name.data = Option.get('office_name')
    return render_template('options/edit.pug', form=form)