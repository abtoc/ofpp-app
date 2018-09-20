from flask_script import Manager
from flaskr import db
from flaskr.models import Person

ExportCommand = Manager(usage='データをエクスポートするコマンドです')

@ExportCommand.command
def persons():
    items = Person.query.order_by(Person.id).all()
    for item in items:
        print('"{}","{}","{}","{}","{}"'.format(
            item.id,
            item.name,
            item.idm if bool(item.idm) else '',
            item.create_at if bool(item.create_at) else '',
            item.update_at if bool(item.update_at) else ''
        ))
