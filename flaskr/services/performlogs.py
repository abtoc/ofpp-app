from flask import url_for, abort
from flaskr import db
from flaskr.models import PerformLog
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
        self.sync_to_worklog(worklog)
        db.session.commit()
    def sync_from_worklog(self, worklog):
        self.absence = False
        self.absence_add = False
        self.work_in = worklog.work_in
        self.work_out = worklog.work_out
        self.company_id = worklog.company_id
        self.presented = self.is_presented(worklog)
        self.enabled = self.is_enabled()
        db.session.add(self)
        absencelog = AbsenceLog.query.get((self.person_id, self.yymm, self.dd))
        if bool(absencelog):
            db.session.delete(absencelog)
    def sync_to_worklog(self, worklog):
        worklog.work_in = self.work_in
        worklog.work_out = self.work_out
        worklog.company_id = self.company_id
        worklog.absence = self.absence
        worklog.presented = bool(worklog.work_in) or bool(worklog.work_out) or bool(worklog.value)
        db.session.add(worklog)
    def delete(self):
        if bool(self.absencelog):
            db.session.delete(self.absencelog)
        worklog = WorkLog.query.get((self.person_id, self.yymm, self.dd))
        if worklog is not None:
            db.session.delete(worklog)
        db.session.delete(self)
        db.session.commit()
