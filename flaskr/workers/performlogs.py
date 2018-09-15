from datetime import date
from dateutil.relativedelta import relativedelta
from flaskr import app, db, celery
from flaskr.models import Person, PerformLog

@celery.task
def update_performlogs_enabled(id, yymm):
    app.logger.info('Update PerformLog enabled. id={} yymm={}'.format(id, yymm))
    person = Person.query.get(id)
    if person is None:
        return
    yy = int(yymm[:4])
    mm = int(yymm[4:])
    last = date(yy,mm,1)
    last += relativedelta(months=1)
    last -= relativedelta(days=1)
    last = last.day - 8
    logs = PerformLog.query.filter(
        PerformLog.person_id == id,
        PerformLog.yymm == yymm
    ).order_by(
        PerformLog.person_id,
        PerformLog.yymm,
        PerformLog.dd
    ).all()
    count = 0
    for log in logs:
        if log.presented:
            count = count + 1
            if count > last:
                log.presented = False
                log.enabled = False
                db.session.add(log)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.exception(e)

                