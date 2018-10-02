from collections import namedtuple
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint, redirect, render_template, url_for
from flaskr.services.summarys import SummaryService
from flaskr.utils.datetime import date_x
from flaskr.utils.roles import login_required_staff

bp = Blueprint('summarys', __name__, url_prefix='/summarys')

@bp.route('/')
@login_required_staff
def default():
    return redirect(url_for('summarys.index', yymm=date.today().strftime('%Y%m')))

def make_foot(items):
    Foot = namedtuple('foot', ('usedate', 'absence_add',  'outemp', 'presented', 'value', 'absence', 'late', 'leave'))
    foot = Foot(
        sum([item.usedate for item in items if item.usedate is not None]),
        sum([item.absence_add for item in items if item.absence_add is not None]),
        sum([item.outemp for item in items if item.outemp is not None]),
        sum([item.presented for item in items if item.presented is not None]),
        sum([item.value for item in items if item.value is not None]),
        sum([item.absence for item in items if item.absence is not None]),
        sum([item.late for item in items if item.late is not None]),
        sum([item.leave for item in items if item.leave is not None]),
    )
    return foot

@bp.route('/<yymm>')
@login_required_staff
def index(yymm):
    today = date_x.yymm_dd(yymm, 1)
    first = today
    last = first + relativedelta(months=1)
    prev = first - relativedelta(months=1)
    this = date_x()
    items = SummaryService.get_all(yymm)
    foot = make_foot(items)
    kw = dict(
        yymm = yymm,
        today = today.date,
        prev = prev.date.strftime('%Y%m'),
        next = last.date.strftime('%Y%m'),
        this = this.date.strftime('%Y%m'),
        items = items,
        foot = foot
    )
    return render_template('summarys/index.pug', **kw)

@bp.route('/<yymm>/report')
@login_required_staff
def report(yymm):
    today = date_x.yymm_dd(yymm, 1)
    items = SummaryService.get_all(yymm)
    foot = make_foot(items)
    kw = dict(
        yymm = yymm,
        today = today.date,
        items = items,
        foot = foot
    )
    return render_template('summarys/report.pug', **kw)
