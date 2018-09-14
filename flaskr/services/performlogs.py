from flask import url_for, abort
from flaskr import db
from flaskr.models import PerformLog
from flaskr.services import worklogs
from flaskr.models import AbsenceLog, WorkLog

class PerformLogService(PerformLog):
    def __is_presented(self, worklog):
        if bool(self.work_in):
            return True
        if bool(self.work_out):
            return True
        if worklog.value is not None:
            return True
        return False
    def __is_enabled(self, worklog):
        if self.__is_presented(worklog):
            return True
        if self.absence_add:
            return True
        if (self.pickup_in) and (self.pikup_out):
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
        if not bool(self.work_in):
            self.work_in = None
        if not bool(self.work_out):
            self.work_out = None
        if not bool(self.remarks):
            self.remarks = None
        worklog = worklogs.WorkLogService.get_or_new(self.person_id, self.yymm, self.dd)
        self.enabled = self.__is_enabled(worklog)
        self.presented = self.__is_presented(worklog)
        db.session.add(self)
        if bool(self.absencelog):
            self.absencelog.deleted = not self.absence_add
            db.session.add(self.absencelog)
        elif self.absence_add:
            absencelog = AbsenceLog(person_id=self.person_id, yymm=self.yymm, dd=self.dd)
            db.session.add(absencelog)
        db.session.commit()
        # update_performlog_enabled.delay(self.person_id, self.yymm)
        worklog.update_performlog(self)
    def sync_worklog(self, worklog):
        self.absence = False
        self.absence_add = False
        self.work_in = worklog.work_in
        self.work_out = worklog.work_out
        self.presented = self.__is_presented(worklog)
        self.enabled = self.__is_enabled(worklog)
        db.session.add(self)
        if bool(self.absencelog):
            self.absencelog.deleted = not self.absence_add
            db.session.add(self.absencelog)
        elif self.absence_add:
            absencelog = AbsenceLogService(self.person_id, self.yymm, self.dd)
            db.session.add(absencelog)
        #update_performlog_enabled.delay(self.person_id, self.yymm)
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
