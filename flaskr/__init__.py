from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from werkzeug.contrib.cache import SimpleCache
import pymysql
pymysql.install_as_MySQLdb

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('flaskr.config')
app.config.from_pyfile('config.py', silent=True)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'
lm.login_message = 'ユーザID、パスワードを入力してください'
lm.login_message_category = 'warning'

auth = HTTPBasicAuth()

cache = SimpleCache()

celery = make_celery(app)

import flaskr.models
import flaskr.helpers
import flaskr.views
import flaskr.apis
import flaskr.reports
import flaskr.workers
