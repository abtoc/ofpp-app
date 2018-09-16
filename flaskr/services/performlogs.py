from flask import url_for, abort
from flaskr import db
from flaskr.models import PerformLog
from flaskr.workers.performlogs import update_performlogs_enabled
from flaskr.workers.worklogs import update_worklogs_value
from flaskr.models import AbsenceLog, WorkLog

class PerformLogService(PerformLog):
    def is_presented(self, worklog):
        if bool(self.work_in):
            return True
        if bool(self.work_out):
            return True
        if worklog.value is not None:
            return True
        return False
    def is_enabled(self):
        if self.presented:
            return True
        if self.absence_add:
            return True
        if (self.pickup_in) or (self.pickup_out):
            return True
        if self.visit:
            return True
        if self.meal:
            return True
        if bool(self.medical):
            return True
        if bool(self.experience):
            return True
        if self.outside:
            return True
        return False        
    def update(self, form):
        form.populate_obj(self)
        worklog = WorkLog.get_or_new(self.person_id, self.yymm, self.dd)
        self.presented = self.is_presented(worklog)
        self.enabled = self.is_enabled()
        db.session.add(self)
        absencelog = AbsenceLog.query.get((self.person_id, self.yymm, self.dd))
        if bool(absencelog) and (not self.absence_add):
            db.session.delete(absencelog)
        elif (not bool(absencelog)) and self.absence_add:
            absencelog = AbsenceLog(person_id=self.person_id, yymm=self.yymm, dd=self.dd)
            db.session.add(absencelog)
        db.session.commit()
        self.update_to_worklog(worklog)
        update_performlogs_enabled.delay(self.person_id, self.yymm)
    def sync_from_worklog(self, worklog):
        self.absence = False
        self.absence_add = False
        self.work_in = worklog.work_in
        self.work_out = worklog.work_out
        self.presented = self.is_presented(worklog)
        self.enabled = self.is_enabled()
        db.session.add(self)
        absencelog = AbsenceLog.query.get((self.person_id, self.yymm, self.dd))
        if bool(absencelog):
            db.session.delete(absencelog)
    def update_to_worklog(self, worklog):
        worklog.work_in = self.work_in
        worklog.work_out = self.work_out
        worklog.absence = self.absence
        worklog.presented = bool(worklog.work_in) or bool(worklog.work_out) or bool(worklog.value)
        db.session.add(worklog)
        db.session.commit()
        update_worklogs_value.delay(worklog.person_id, worklog.yymm, worklog.dd)
    def delete(self):
        if bool(self.absencelog):
            db.session.delete(self.absencelog)
        worklog = WorkLog.query.get((self.person_id, self.yymm, self.dd))
        if worklog is not None:
            db.session.delete(worklog)
        db.session.delete(self)
        db.session.commit()
    @property
    def url_edit(self):
        return url_for('performlogs.edit', id=self.person_id, yymm=self.yymm, dd=self.dd)
    @property
    def url_delete(self):
        if self.enabled is None:
            return url_for('performlogs.index', id=self.person_id, yymm=self.yymm)
        return url_for('performlogs.destroy', id=self.person_id, yymm=self.yymm, dd=self.dd)
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
