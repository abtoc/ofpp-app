#!/usr/bin/env python
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flaskr import app, db
import pymysql
pymysql.install_as_MySQLdb()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from commands import ApplicationCommand
from commands import ExportCommand
manager.add_command('app', ApplicationCommand)
manager.add_command('export', ExportCommand)

if __name__ == '__main__':
    manager.run()
