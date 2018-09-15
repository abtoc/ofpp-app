from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from flaskr.forms.timerules import TimeRuleForm
from flaskr.services.timerules import TimeRuleService
from flaskr.models import TimeRule
from flaskr import db

bp = Blueprint('timerules', __name__, url_prefix='/timerules')

@bp.route('/')
@login_required
def index():
    items = TimeRuleService.query.order_by(TimeRule.caption).all()
    return render_template('timerules/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TimeRuleForm()
    if form.validate_on_submit():
        timerule = TimeRuleService()
        try:
            timerule.update(form)
            flash('タイムテーブルの登録ができました', 'success')
            return redirect(url_for('timerules.index'))
        except ValueError as e:
            db.session.rollback()
            flash(e, 'danger')
        except Exception as e:
            db.session.rollback()
            flash('タイムテーブル登録時にエラーが出ました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc)
    return render_template('timerules/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    timerule = TimeRuleService.get_or_404(id)
    form = TimeRuleForm(obj=timerule)
    if form.validate_on_submit():
        try:
            timerule.update(form)
            flash('タイムテーブルの更新ができました', 'success')
            return redirect(url_for('timerules.index'))
        except ValueError as e:
            db.session.rollback()
            flash(e, 'danger')
        except Exception as e:
            db.session.rollback()
            flash('タイムテーブル更新時にエラーが出ました {}'.format(e), 'danger')
            from traceback import format_exc
            print(format_exc)
    return render_template('timerules/edit.pug', id=id, form=form)

@bp.route('/<id>/destroy')
@login_required
def destroy(id):
    timerule = TimeRuleService.get_or_404(id)
    try:
        timerule.delete()
        flash('タイムテーブルの削除ができました')
    except Exception as e:
        db.session.rollback()
        flash('タイムテーブル削除時にエラーが発生しました {}'.format(e), 'danger')
        from traceback import format_exc
        print(format_exc())
    return redirect(url_for('timerules.index'))
