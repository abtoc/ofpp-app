#!/usr/bin/env python
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flaskr import app, db
import pymysql
pymysql.install_as_MySQLdb()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from commands.application import ApplicationCommand
manager.add_command('app', ApplicationCommand)

if __name__ == '__main__':
    manager.run()
