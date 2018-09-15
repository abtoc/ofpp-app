from flask import url_for, abort
from flaskr import db
from flaskr.models import WorkLog, PerformLog
from flaskr.services import performlogs
from flaskr.workers.worklogs import update_worklogs_value
from flaskr.workers.performlogs import update_performlogs_enabled

class WorkLogService(WorkLog):
    def update_staff(self, form):
        form.populate_obj(self)
        if not bool(self.work_in):
            self.work_in = None
        if not bool(self.work_out):
            self.work_out = None
        if not bool(self.remarks):
            self.remarks = None
        if self.value is not None:
            self.presented = True
        else:
            self.presented = False
        db.session.add(self)
        db.session.commit()
        update_worklogs_value.delay(self.person_id, self.yymm, self.dd)
    def update_no_staff(self, form):
        form.populate_obj(self)
        if not bool(self.remarks):
            self.remarks = None
        if self.value is not None:
            self.presented = True
        else:
            self.presented = False
        db.session.add(self)
        performlog = performlogs.PerformLogService.get_or_new(self.person_id, self.yymm, self.dd)
        performlog.sync_worklog(self)
        db.session.commit()
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
            performlog = performlogs.PerformLogService.get_or_new(self.person_id, self.yymm, self.dd)
            performlog.sync_worklog(self)
        db.session.commit()
        update_worklogs_value.delay(self.person_id, self.yymm, self.dd)
        if not self.person.staff:
            update_performlogs_enabled.delay(self.person_id, self.yymm)
    def update_performlog(self, performlog):
        self.work_in = performlog.work_in
        self.work_out = performlog.work_out
        self.absence = performlog.absence
        self.presented = bool(self.work_in) or bool(self.work_out)
        db.session.add(self)
        db.session.commit()
        update_worklogs_value.delay(self.person_id, self.yymm, self.dd)
    def delete(self):
        if not self.person.staff:
            raise ValueError('利用者の勤怠削除は実績登録から削除してください')
        db.session.delete(self)
        db.session.commit()
    @property
    def url_edit(self):
        return url_for('worklogs.edit', id=self.person_id, yymm=self.yymm, dd=self.dd)
    @property
    def url_delete(self):
        return url_for('worklogs.destory', id=self.person_id, yymm=self.yymm, dd=self.dd)
    @classmethod
    def get_or_new(cls, id, yymm, dd):
        result = cls.query.get((id, yymm, dd))
        if result is None:
            result = cls(person_id=id, yymm=yymm, dd=dd)
        return result
    @classmethod
    def get_or_404(cls, id, yymm, dd):
        result = cls.query.get((id, yymm, dd))
        if result is None:
            abort(404)
        return result
    @classmethod
    def get_date(cls, id, d):
        yymm = d.strftime('%Y%m')
        dd = d.day
        return cls.query.get((id, yymm, dd))
