from dateutil.relativedelta import relativedelta
from collections import namedtuple
from flask_login import login_required
from collections import namedtuple
from io import BytesIO
from flask import Blueprint, render_template, redirect, url_for, flash, make_response, abort
from flaskr.forms.worklogs import WorkLogForm, WorkLogFormStaff
from flaskr.services.worklogs import WorkLogService
from flaskr.reports.worklogs import WorkLogReport
from flaskr import app, db
from flaskr.models import Person
from flaskr.utils.datetime import date_x

bp = Blueprint('worklogs', __name__, url_prefix="/worklogs")

@bp.route('/<id>/<yymm>')
@login_required
def index(id, yymm):
    person = Person.get_or_404(id)
    today = date_x.yymm_dd(yymm, 1)
    first = today
    last = first + relativedelta(months=1)
    prev = first - relativedelta(months=1)
    this = date_x()
    items = []
    while first.date < last.date:
        ym = first.date.strftime('%Y%m')
        d = first.date.day
        worklog = WorkLogService.get_or_new(id, ym, d)
        items.append(worklog)
        first += relativedelta(days=1)
    Foot = namedtuple('Foor', ('presented', 'value', 'break_t', 'over_t', 'absence', 'late', 'leave'))
    foot = Foot(
        len([i for i in items if i.presented]),
        sum([i.value for i in items if i.value is not None]),
        sum([i.break_t for i in items if i.break_t is not None]),
        sum([i.over_t for i in items if i.over_t is not None]),
        len([i for i in items if i.absence]),
        len([i for i in items if i.late]),
        len([i for i in items if i.leave]),
    )
    kw = dict(
        id = id,
        yymm = yymm,
        staff = person.staff,
        name = person.name,
        today = today.date,
        this = this.date.strftime('%Y%m'),
        prev = prev.date.strftime('%Y%m'),
        next = last.date.strftime('%Y%m'),
        items = items,
        foot = foot
    )
    return render_template('worklogs/index.pug', **kw)

@bp.route('/<id>/<yymm>/<dd>/edit', methods=['GET', 'POST'])
@login_required
def edit(id, yymm, dd):
    try:
        date_x.yymm_dd(yymm, dd)
    except:
        abort(400)
    person = Person.get_or_404(id)
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
@login_required
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

@bp.route('/<id>/<yymm>/report')
@login_required
def report(id, yymm):
    with BytesIO() as output:
        report = WorkLogReport(id, yymm)
        report(output)
        response = make_response(output.getvalue())
        response.mimetype = 'application/pdf'
    return response
