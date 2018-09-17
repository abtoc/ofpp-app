from flask import url_for, abort
from flaskr import db
from flaskr.models import WorkLog, PerformLog
from flaskr.services.performlogs import PerformLogService

class WorkLogService(WorkLog):
    def update_staff(self, form):
        form.populate_obj(self)
        if self.value is not None:
            self.presented = True
        else:
            self.presented = False
        db.session.add(self)
        db.session.commit()
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
    def delete(self):
        if not self.person.staff:
            raise ValueError('利用者の勤怠削除は実績登録から削除してください')
        db.session.delete(self)
        db.session.commit()
