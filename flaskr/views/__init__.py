from flask import render_template
from flaskr import app

@app.route('/')
def index():
    return render_template('index.pug')

from flaskr.views.persons import bp
app.register_blueprint(persons.bp)
