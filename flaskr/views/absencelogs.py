from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template, redirect, url_for, flash, make_response
from io import BytesIO
from flaskr.forms.absencelogs import AbsenseLogForm
from flaskr.reports.absencelogs import AbsenceLogReport
from flaskr.models import AbsenceLog
from flaskr import app, db
from flaskr.utils.datetime import date_x
from flaskr.utils.roles import login_required_staff

bp = Blueprint('absencelogs', __name__, url_prefix='/absencelogs')

@bp.route('/')
@login_required_staff
def default():
    return redirect(url_for('absencelogs.index', yymm=date.today().strftime('%Y%m')))

@bp.route('/<yymm>')
@login_required_staff
def index(yymm):
    items = AbsenceLog.query.filter(
        AbsenceLog.yymm==yymm
    ).order_by(
        AbsenceLog.yymm,
        AbsenceLog.dd
    ).all()
    today = date_x.yymm_dd(yymm, 1)
    first = today
    last = first + relativedelta(months=1)
    prev = first - relativedelta(months=1)
    this = date.today()
    kw = dict(
        yymm = yymm,
        today = today.date,
        prev = prev.date.strftime('%Y%m'),
        next = last.date.strftime('%Y%m'),
        this = this.strftime('%Y%m'),
        items = items
    )
    return render_template('absencelogs/index.pug', **kw)

@bp.route('/<id>/<yymm>/<dd>', methods=['GET', 'POST'])
@login_required_staff
def edit(id, yymm, dd):
    item = AbsenceLog.get_or_404((id, yymm, dd))
    form = AbsenseLogForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('欠席時対応加算記録を更新しました','success')
            return redirect(url_for('absencelogs.index', yymm=yymm))
        except Exception as e:
            db.session.rollback()
            flash('欠席時対応加算記録更新時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('absencelogs/edit.pug', item=item, form=form)

@bp.route('/<yymm>/report')
@login_required_staff
def report(yymm):
    with BytesIO() as output:
        report = AbsenceLogReport(yymm)
        report(output)
        response = make_response(output.getvalue())
        response.mimetype = 'application/pdf'
    return response
