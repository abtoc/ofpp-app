from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash
from flaskr.services.absencelogs import AbsenceLogService
from flaskr.forms.absencelogs import AbsenseLogForm
from flaskr.models import AbsenceLog
from flaskr import app, db

bp = Blueprint('absencelogs', __name__, url_prefix='/absencelogs')

@bp.route('/')
def default():
    return redirect(url_for('absencelogs.index', yymm=date.today().strftime('%Y%m')))

@bp.route('/<yymm>')
def index(yymm):
    items = AbsenceLogService.query.filter(AbsenceLog.yymm==yymm).all()
    return render_template('absencelogs/index.pug', yymm=yymm, items=items)

@bp.route('/<id>/<yymm>/<dd>', methods=['GET', 'POST'])
def edit(id, yymm, dd):
    absencelog = AbsenceLogService.get_or_404(id, yymm, dd)
    form = AbsenseLogForm(obj=absencelog)
    if form.validate_on_submit():
        try:
            absencelog.update(form)
            flash('欠席時対応加算記録を更新しました','success')
            return redirect(url_for('absencelogs.index', yymm=yymm))
        except Exception as e:
            db.session.rollback()
            flash('欠席時対応加算記録更新時にエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('absencelogs/edit.pug', item=absencelog, form=form)
