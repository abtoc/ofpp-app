from flaskr import app, celery, db
from flaskr.models import Person, WorkLog
from flaskr.services.timerules import TimeRuleService

@celery.task
def update_worklogs_value(id, yymm, dd=None):
    app.logger.info('Update Worklog value from TimeTable. id={} yymm={} dd={}'.format(id, yymm, dd))
    person = Person.query.get(id)
    if person is None:
        return
    if person.timerule_id is None:
        return
    timerule = TimeRuleService.query.get(person.timerule_id)
    if timerule is None:
        return
    if dd is None:
        dd = range(1, 32)
    else:
        dd = (dd,)
    for d in dd:
        log = WorkLog.query.get((id, yymm, d))
        if log is None:
            continue
        if log.value is not None:
            continue
        if not bool(log.work_in):
            continue
        if not bool(log.work_out):
            continue
        app.logger.info('Updating Worklog value from TimeTable. id={} yymm={} dd={}'.format(id, yymm, d))
        log.value, log.break_t, log.over_t, log.late, log.leave = timerule.calc(log.work_in, log.work_out)
        log.presented = True
        db.session.add(log)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.exception(e)
