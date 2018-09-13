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
