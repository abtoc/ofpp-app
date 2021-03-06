from datetime import date
from dateutil.relativedelta import relativedelta
from collections import namedtuple
from io import BytesIO
from flask import Blueprint, render_template, redirect, make_response, url_for, flash, abort
from flaskr.forms.performlogs import PerformLogFormIDM, PerformLogForm
from flaskr.services.performlogs import PerformLogService
from flaskr.services.worklogs import WorkLogService
from flaskr import app, db, cache
from flaskr.utils.datetime import date_x
from flaskr.utils.roles import check_idm
from flaskr.reports.performlogs import PerformLogReport
from flaskr.models import Person
from flaskr.workers.performlogs import update_performlogs_enabled
from flaskr.workers.worklogs import update_worklogs_value
from flaskr.utils.roles import login_required_staff, login_required_person
bp = Blueprint('performlogs', __name__, url_prefix="/performlogs")

@bp.route('/<id>/<yymm>')
@login_required_person
def index(id, yymm):
    person = Person.get_or_404(id)
    if person.staff:
        flash('職員はこの画面はサポートしておりません', 'danger')
        return redirect(url_for('index'))
    today = date_x.yymm_dd(yymm, 1)
    first = today
    last = first + relativedelta(months=1)
    prev = first - relativedelta(months=1)
    this = date.today()
    items = []
    while first.date < last.date:
        ym = first.date.strftime('%Y%m')
        d = first.date.day
        performlog = PerformLogService.get_or_new(id, ym, d)
        items.append(performlog)
        first += relativedelta(days=1)
    Foot = namedtuple('Foot', ('presented', 'pickup', 'visit', 'meal', 'medical', 'experience', 'outemp', 'outside'))
    foot = Foot(
        len([i for i in items if i.presented]),
        len([i for i in items if i.pickup_in]) +
        len([i for i in items if i.pickup_out]),
        len([i for i in items if bool(i.visit) and i.visit > 0]),
        len([i for i in items if i.meal]),
        len([i for i in items if bool(i.medical) and i.medical > 0]),
        len([i for i in items if bool(i.experience) and i.experience > 0]),
        len([i for i in items if bool(i.company_id)]),
        len([i for i in items if i.outside]),
    )
    kw = dict(
        id = id,
        yymm = yymm,
        today = today.date,
        name = person.display_or_name,
        prev = prev.date.strftime('%Y%m'),
        next = last.date.strftime('%Y%m'),
        this = this.strftime('%Y%m'),
        items = items,
        foot = foot
    )
    return render_template('performlogs/index.pug', **kw)

@bp.route('/<id>/<yymm>/<dd>/edit', methods=['GET', 'POST'])
@login_required_staff
def edit(id, yymm, dd):
    try:
        date_x.yymm_dd(yymm, dd)
    except ValueError:
        abort(400)
    person = Person.get_or_404(id)
    if person.staff:
        flash('職員はこの画面はサポートしておりません', 'danger')
        return redirect(url_for('index'))
    performlog = PerformLogService.get_or_new(id, yymm, dd)
    if check_idm(person):
        form = PerformLogFormIDM(obj=performlog)
    else:
        form = PerformLogForm(obj=performlog)
    if form.validate_on_submit():
        try:
            performlog.update(form)
            update_worklogs_value.delay(id, yymm, dd)
            update_performlogs_enabled.delay(id, yymm)
            flash('実績の登録ができました', 'success')
            return redirect(url_for('performlogs.index', id=id, yymm=yymm))
        except Exception as e:
            db.session.rollback()
            flash('実績登録時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    kw = dict(
        id = id,
        yymm = yymm,
        dd = dd,
        form = form,
        item = performlog   
    )
    return render_template('performlogs/edit.pug', **kw)

@bp.route('/<id>/<yymm>/<dd>/destroy')
@login_required_staff
def destroy(id, yymm, dd):
    person = Person.get_or_404(id)
    if person.staff:
        flash('職員はこの画面はサポートしておりません', 'danger')
        return redirect(url_for('index'))
    performlog = PerformLogService.get_or_404((id, yymm, dd))
    worklog = WorkLogService.get_or_404((id, yymm, dd))
    if not check_idm(person):
        if bool(performlog.work_in) or bool(performlog.work_out) or bool(worklog.value):
            flash('利用者のICカードをタッチしてください', 'danger')
            return redirect(url_for('performlogs.index', id=id, yymm=yymm))
    try:
        performlog.delete()
        update_performlogs_enabled.delay(id, yymm)
        flash('実績の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('実績削除時にエラーが出ました {}'.format(e), 'danger')
        app.logger.exception(e)
    return redirect(url_for('performlogs.index', id=id, yymm=yymm))

@bp.route('/<id>/<yymm>/report')
@login_required_person
def report(id, yymm):
    with BytesIO() as output:
        pdf = PerformLogReport(id, yymm)
        pdf(output)
        response = make_response(output.getvalue())
        response.mimetype = 'application/pdf'
    return response

@bp.route('/<id>/<yymm>/update')
@login_required_staff
def update(id, yymm):
    update_performlogs_enabled.delay(id, yymm)
    return redirect(url_for('performlogs.index',id=id, yymm=yymm))
