from collections import namedtuple
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import render_template, url_for
from flask_login import login_required, current_user
from flaskr import app, cache
from flaskr.models import Person
from flaskr.utils.roles import check_idm
from flaskr.services.worklogs import WorkLogService

def _get_caption(person, date):
    worklog = WorkLogService.get_date(person.id, date)
    yymm = date.strftime('%Y%m')
    dd = date.day
    if worklog is None:
        caption = 'ー'
    else:
        if worklog.absence:
            caption = '欠席'
        else:
            caption = '{}−{}'.format(
                worklog.work_in if bool(worklog.work_in) else '',
                worklog.work_out if bool(worklog.work_out) else ''
            )
    return caption

def _get_url(person, date):
    yymm = date.strftime('%Y%m')
    dd = date.day
    if person.staff:
        url = url_for('worklogs.edit', id=person.id, yymm=yymm, dd=dd)
    else:
        url = url_for('performlogs.edit', id=person.id, yymm=yymm, dd=dd)
    return url

@app.route('/')
@login_required
def index():
    today = date.today()
    yesterday1 = today - relativedelta(days=1)
    yesterday2 = today - relativedelta(days=2)
    yesterday3 = today - relativedelta(days=3)
    prev = today - relativedelta(months=1)
    Item = namedtuple('Item', (
           'name',
           'idm',
           'staff',
           'caption',
           'url',
           'caption1',
           'url1',
           'caption2',
           'url2',
           'caption3',
           'url3',
           'url_performlogs',
           'utl_performlogs_report',
           'url_performlogs_report1',
           'url_worklogs',
           'url_worklogs_report',
           'url_worklogs_report1'
        ))
    if current_user.is_staff():
        persons = Person.query.filter(Person.enabled==True).order_by(Person.staff, Person.name).all()
    else:
        persons = (Person.get_or_404(current_user.person_id),)
    items = []
    for person in persons:
        item = Item(
            person.display_or_name,
            check_idm(person),
            person.staff,
            _get_caption(person, today),
            _get_url(person, today),
            _get_caption(person, yesterday1),
            _get_url(person, yesterday1),
            _get_caption(person, yesterday2),
            _get_url(person, yesterday2),
            _get_caption(person, yesterday3),
            _get_url(person, yesterday3),
            url_for('performlogs.index', id=person.id, yymm=today.strftime('%Y%m')),
            url_for('performlogs.report', id=person.id, yymm=today.strftime('%Y%m')),
            url_for('performlogs.report', id=person.id, yymm=prev.strftime('%Y%m')),
            url_for('worklogs.index', id=person.id, yymm=today.strftime('%Y%m')),
            url_for('worklogs.report', id=person.id, yymm=today.strftime('%Y%m')),
            url_for('worklogs.report', id=person.id, yymm=prev.strftime('%Y%m')),
        )
        items.append(item)
    return render_template('index.pug', items=items)

from flaskr.views.persons import bp
app.register_blueprint(persons.bp)
from flaskr.views.recipients import bp
app.register_blueprint(recipients.bp)
from flaskr.views.staffs import bp
app.register_blueprint(staffs.bp)
from flaskr.views.timerules import bp
app.register_blueprint(timerules.bp)
from flaskr.views.users import bp
app.register_blueprint(users.bp)
from flaskr.views.options import bp
app.register_blueprint(options.bp)
from flaskr.views.worklogs import bp
app.register_blueprint(worklogs.bp)
from flaskr.views.performlogs import bp
app.register_blueprint(performlogs.bp)
from flaskr.views.absencelogs import bp
app.register_blueprint(absencelogs.bp)
from flaskr.views.auth import bp
app.register_blueprint(auth.bp)
from flaskr.views.summarys import bp
app.register_blueprint(summarys.bp)
