from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from flaskr.forms.timerules import TimeRuleForm
from flaskr.models import TimeRule
from flaskr import app, db

bp = Blueprint('timerules', __name__, url_prefix='/timerules')

@bp.route('/')
@login_required
def index():
    items = TimeRule.query.order_by(TimeRule.caption).all()
    return render_template('timerules/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TimeRuleForm()
    if form.validate_on_submit():
        item = TimeRule()
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('タイムテーブルの登録ができました', 'success')
            return redirect(url_for('timerules.index'))
        except Exception as e:
            db.session.rollback()
            flash('タイムテーブル登録時にエラーが出ました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('timerules/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = TimeRule.get_or_404(id)
    form = TimeRuleForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('タイムテーブルの更新ができました', 'success')
            return redirect(url_for('timerules.index'))
        except Exception as e:
            db.session.rollback()
            flash('タイムテーブル更新時にエラーが出ました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('timerules/edit.pug', id=id, form=form)

@bp.route('/<id>/destroy')
@login_required
def destroy(id):
    item = TimeRule.get_or_404(id)
    db.session.delete(item)
    try:
        db.session.commit()
        flash('タイムテーブルの削除ができました')
    except Exception as e:
        db.session.rollback()
        flash('タイムテーブル削除時にエラーが発生しました {}'.format(e), 'danger')
        app.logger.exception(e)
    return redirect(url_for('timerules.index'))
