from flask import render_template
from flaskr import app

@app.route('/')
def index():
    return render_template('index.pug')

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
