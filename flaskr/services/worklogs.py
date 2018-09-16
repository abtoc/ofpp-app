from flask import url_for, abort
from flaskr import db
from flaskr.models import WorkLog, PerformLog
from flaskr.services.performlogs import PerformLogService
from flaskr.workers.worklogs import update_worklogs_value
from flaskr.workers.performlogs import update_performlogs_enabled

class WorkLogService(WorkLog):
    def update_staff(self, form):
        form.populate_obj(self)
        if self.value is not None:
            self.presented = True
        else:
            self.presented = False
        db.session.add(self)
        db.session.commit()
        update_worklogs_value.delay(self.person_id, self.yymm, self.dd)
    def update_no_staff(self, form):
        form.populate_obj(self)
        if self.value is not None:
            self.presented = True
        else:
            self.presented = False
        db.session.add(self)
        performlog = PerformLogService.get_or_new(self.person_id, self.yymm, self.dd)
        performlog.sync_from_worklog(self)
        db.session.commit()
        update_worklogs_value.delay(self.person_id, self.yymm, self.dd)
        update_performlogs_enabled.delay(self.person_id, self.yymm)
    def update_api(self, tm):
        hhmm = tm.strftime('%H:%M')
        if bool(self.work_in):
            self.work_out = hhmm
            self.value = None
        else:
            self.work_in = hhmm
        self.presented = True
        self.absence = False
        db.session.add(self)
        if not self.person.staff:
            performlog = PerformLogService.get_or_new(self.person_id, self.yymm, self.dd)
            performlog.sync_from_worklog(self)
        db.session.commit()
        update_worklogs_value.delay(self.person_id, self.yymm, self.dd)
        if not self.person.staff:
            update_performlogs_enabled.delay(self.person_id, self.yymm)
    def delete(self):
        if not self.person.staff:
            raise ValueError('利用者の勤怠削除は実績登録から削除してください')
        db.session.delete(self)
        db.session.commit()
