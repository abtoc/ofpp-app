from dateutil.relativedelta import relativedelta
from collections import namedtuple
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flaskr.forms.performlogs import PerformLogFormIDM, PerformLogFormIDM
from flaskr.services.performlogs import PerformLogService
from flaskr.services.persons import PersonService
from flaskr import app, db
from flaskr.utils.datetime import date_x

bp = Blueprint('performlogs', __name__, url_prefix="/performlogs")

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
        performlog = PerformLogService.get_or_new(id, ym, d)
        items.append(performlog)
        first += relativedelta(days=1)
    kw = dict(
        id = id,
        yymm = yymm,
        today = today.date,
        prev = prev.date.strftime('%Y%m'),
        next = last.date.strftime('%Y%m'),
        items = items
    )
    return render_template('performlogs/index.pug', **kw)

@bp.route('/<id>/<yymm>/<dd>/edit', methods=['GET', 'POST'])
def edit(id, yymm, dd):
    try:
        date_x.yymm_dd(yymm, dd)
    except:
        abort(400)
    person = PersonService.get_or_404(id)
    performlog = PerformLogService.get_or_new(id, yymm, dd)
    form = PerformLogFormIDM(obj=performlog)
    if form.validate_on_submit():
        try:
            performlog.update(form)
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
def destroy(id, yymm, dd):
    performlog = PerformLogService.get_or_404(id, yymm, dd)
    try:
        performlog.delete()
        flash('実績の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('実績削除時にエラーが出ました {}'.format(e), 'danger')
        app.logger.exception(e)
    return redirect(url_for('performlogs.index', id=id, yymm=yymm))
