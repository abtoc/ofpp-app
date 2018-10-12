from flask import Blueprint, render_template, redirect, url_for, flash
from flaskr import app, db
from flaskr.forms.agrees import AgreeForm
from flaskr.models import Agree
from flaskr.utils.roles import login_required_staff

bp = Blueprint('agrees', __name__, url_prefix='/agrees')

@bp.route('/')
@login_required_staff
def index():
    items = Agree.query.order_by(
        Agree.agree_out.desc(),
        Agree.caption.asc()
    ).all()
    return render_template('agrees/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required_staff
def create():
    form = AgreeForm()
    if form.validate_on_submit():
        item = Agree()
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('契約情報の登録ができました', 'success')
            return redirect(url_for('agrees.index'))
        except Exception as e:
            db.session.rollback()
            flash('契約情報登録時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('agrees/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required_staff
def edit(id):
    item = Agree.get_or_404(id)
    form = AgreeForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('契約情報の変更ができました', 'success')
            return redirect(url_for('agrees.index'))
        except Exception as e:
            db.session.rollback()
            flash('契約情報変更時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('agrees/edit.pug', id=id, form=form)

@bp.route('/<id>/destroy')
@login_required_staff
def destroy(id):
    item = Agree.get_or_404(id)
    db.session.delete(item)
    try:
        db.session.commit()
        flash('契約情報の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('契約情報削除時にエラーが発生しました {}'.format(e), 'danger')
        app.logger.exception(e)
    return redirect(url_for('agrees.index'))