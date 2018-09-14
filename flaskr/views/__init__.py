from collections import namedtuple
from dateutil.relativedelta import relativedelta
from flask import render_template, url_for
from flaskr import app
from flaskr.models import Person
from flaskr.utils.datetime import date_x

@app.route('/')
def index():
    today = date_x()
    yesterday1 = today - relativedelta(days=1)
    yesterday2 = today - relativedelta(days=2)
    Item = namedtuple('Item', (
           'name',
           'staff',
           'url_performlogs',
           'url_worklogs'
        ))
    persons = Person.query.filter(Person.enabled==True).order_by(Person.staff, Person.name).all()
    items = []
    for person in persons:
        item = Item(
            person.display_or_name,
            person.staff,
            url_for('performlogs.index', id=person.id, yymm=today.date.strftime('%Y%m')),
            url_for('worklogs.index', id=person.id, yymm=today.date.strftime('%Y%m'))
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
