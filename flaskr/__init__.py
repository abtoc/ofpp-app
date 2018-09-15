from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('flaskr.config')
app.config.from_pyfile('config.py', silent=True)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

db = SQLAlchemy(app)

import flaskr.models
import flaskr.helpers
import flaskr.views
import flaskr.apis
