from traceback import format_exc
from flask_script import Manager
from flaskr import db
from flaskr.models import User, TimeRule

ApplicationCommand = Manager(usage='アプリの設定に関するコマンドです')

def add_user(userid, password):
    user = User.query.filter(User.userid == userid).first()
    if user is not None:
        return
    print('ユーザ"{}"追加'.format(userid))
    user = User(userid=userid)
    user.set_password(password)
    user.enabled = True
    user.admin = True
    user.staff = True
    db.session.add(user)
    db.session.commit()

def add_timerule(caption, rules):
    timerule = TimeRule.query.filter(TimeRule.caption == caption).first()
    if timerule is not None:
        return
    print('タイムルール"{}"初期化'.format(caption))
    timerule = TimeRule(caption=caption, rules=rules)
    db.session.add(timerule)
    db.session.commit()

@ApplicationCommand.command
def init():
    """
    アプリケーション初期化
    """
    print('アプリケーション初期化開始')
    print('アカウント初期化')
    add_user('admin', 'password')
    print('タイムルール初期化')
    add_timerule('00:標準', default_rule)
    add_timerule('10:職員', default_rule_staff)

default_rule_staff='''
{
  "times": [
     { "caption": "09:00", "start": "00:00", "end": "09:15", "in": true,  "out": true,  "value":  9.0 },
     { "caption": "09:30", "start": "09:15", "end": "09:45", "in": true,  "out": true,  "value":  9.5 },
     { "caption": "10:00", "start": "09:45", "end": "10:15", "in": true,  "out": true,  "value": 10.0 },
     { "caption": "10:30", "start": "10:15", "end": "10:45", "in": true,  "out": true,  "value": 10.5 },
     { "caption": "11:00", "start": "10:45", "end": "11:15", "in": true,  "out": true,  "value": 11.0 },
     { "caption": "11:30", "start": "11:15", "end": "11:45", "in": true,  "out": true,  "value": 11.5 },
     { "caption": "12:00", "start": "11:45", "end": "13:15", "in": false, "out": true,  "value": 12.0 },
     { "caption": "13:00", "start": "11:45", "end": "13:15", "in": true,  "out": false, "value": 13.0 },
     { "caption": "13:30", "start": "13:15", "end": "13:45", "in": true,  "out": true,  "value": 13.5 },
     { "caption": "14:00", "start": "13:45", "end": "14:15", "in": true,  "out": true,  "value": 14.0 },
     { "caption": "14:30", "start": "14:15", "end": "14:45", "in": true,  "out": true,  "value": 14.5 },
     { "caption": "15:00", "start": "14:45", "end": "15:15", "in": true,  "out": true,  "value": 15.0 },
     { "caption": "15:30", "start": "15:15", "end": "15:45", "in": true,  "out": true,  "value": 15.5 },
     { "caption": "16:00", "start": "16:45", "end": "16:15", "in": true,  "out": true,  "value": 16.0 },
     { "caption": "16:30", "start": "16:15", "end": "16:45", "in": true,  "out": true,  "value": 16.5 },
     { "caption": "17:00", "start": "17:45", "end": "17:15", "in": true,  "out": true,  "value": 17.0 },
     { "caption": "17:30", "start": "17:15", "end": "17:45", "in": true,  "out": true,  "value": 17.5 },
     { "caption": "18:00", "start": "17:45", "end": "23:59", "in": true,  "out": true,  "value": 18.0 }
   ],
  "core": { "start": 9.0, "end": 18.0, "value": 8.0 },
  "break": [
    { "start": 12.0, "end": 13.0, "value": 1.0 }
  ]
}
'''.strip()
default_rule='''
{
  "times": [
     { "caption": "10:00", "start": "00:45", "end": "10:15", "in": true,  "out": true,  "value": 10.0 },
     { "caption": "10:30", "start": "10:15", "end": "10:45", "in": true,  "out": true,  "value": 10.5 },
     { "caption": "11:00", "start": "10:45", "end": "11:15", "in": true,  "out": true,  "value": 11.0 },
     { "caption": "11:30", "start": "11:15", "end": "11:45", "in": true,  "out": true,  "value": 11.5 },
     { "caption": "12:00", "start": "11:45", "end": "13:15", "in": false, "out": true,  "value": 12.0 },
     { "caption": "13:00", "start": "11:45", "end": "13:15", "in": true,  "out": false, "value": 13.0 },
     { "caption": "13:30", "start": "13:15", "end": "13:45", "in": true,  "out": true,  "value": 13.5 },
     { "caption": "14:00", "start": "13:45", "end": "14:15", "in": true,  "out": true,  "value": 14.0 },
     { "caption": "14:30", "start": "14:15", "end": "14:45", "in": true,  "out": true,  "value": 14.5 },
     { "caption": "15:00", "start": "14:45", "end": "23:59", "in": true,  "out": true,  "value": 15.0 }
   ],
  "core": { "start": 10.0, "end": 15.0, "value": 4.0 },
  "break": [
    { "start": 12.0, "end": 13.0, "value": 1.0 }
  ]
}
'''.strip()
