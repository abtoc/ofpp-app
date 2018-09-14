from dateutil.relativedelta import relativedelta
from collections import namedtuple
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flaskr.forms.worklogs import WorkLogForm, WorkLogFormStaff
from flaskr.services.worklogs import WorkLogService
from flaskr.services.persons import PersonService
from flaskr import app, db
from flaskr.utils.datetime import date_x

bp = Blueprint('worklogs', __name__, url_prefix="/worklogs")

@bp.route('/<id>/<yymm>')
def index(id, yymm):
    person = PersonService.get_or_404(id)
    today = date_x.yymm_dd(yymm, 1)
    first = today
    last = first + relativedelta(months=1)
    prev = first - relativedelta(months=1)
    items = []
    while first.date < last.date:
        ym = first.date.strftime('%Y%m')
        d = first.date.day
        worklog = WorkLogService.get_or_new(id, ym, d)
        items.append(worklog)
        first += relativedelta(days=1)
    kw = dict(
        id = id,
        yymm = yymm,
        today = today.date,
        prev = prev.date.strftime('%Y%m'),
        next = last.date.strftime('%Y%m'),
        items = items
    )
    return render_template('worklogs/index.pug', **kw)

@bp.route('/<id>/<yymm>/<dd>/edit', methods=['GET', 'POST'])
def edit(id, yymm, dd):
    try:
        date_x.yymm_dd(yymm, dd)
    except:
        abort(400)
    person = PersonService.get_or_404(id)
    worklog = WorkLogService.get_or_new(id, yymm, dd)
    if person.staff:
        form = WorkLogFormStaff(obj=worklog)
    else:
        form = WorkLogForm(obj=worklog)
    if form.validate_on_submit():
        try:
            if person.staff:
                worklog.update_staff(form)
            else:
                worklog.update_no_staff(form)
            flash('勤怠の登録ができました', 'success')
            return redirect(url_for('worklogs.index', id=id, yymm=yymm))
        except Exception as e:
            db.session.rollback()
            flash('勤怠登録時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    kw = dict(
        id = id,
        yymm = yymm,
        dd = dd,
        form = form,
        item = worklog
    )
    return render_template('worklogs/edit.pug', **kw)

@bp.route('/<id>/<yymm>/<dd>/destroy')
def destory(id, yymm, dd):
    worklog = WorkLogService.get_or_404(id, yymm, dd)
    try:
        worklog.delete()
        flash('勤怠の削除ができました', 'success')
    except ValueError as e:
        db.session.rollback()
        flash(str(e), 'danger')
    except Exception as e:
        db.session.rollback()
        flash('勤怠削除時にエラーが発生しました {}'.format(e), 'danger')
        app.logger.exception(e)
    return redirect(url_for('worklogs.index', id=id, yymm=yymm))
