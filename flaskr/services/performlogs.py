from flaskr import db
from flaskr.models import PerformLog
from flaskr.services.absencelogs import AbsenceLogService

class PerformLogService(PerformLog):
    def __is_presented(worklog):
        if bool(self.work_in):
            return True
        if bool(self.work_out):
            return True
        if self.value is not None:
            return True
        return False
    def __is_enabled(worklog):
        if __is_presented(worklog):
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
        worklog = WorkLogService.get_or_new(self.person_id, self.yymm, self.dd)
        self.enabled = __is_enabled(worklog)
        self.presented = __is_presented(worklog)
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
    def update__worklog(self, worklog):
        self.absence = False
        self.absence_add = False
        self.work_in = worklog.work_in
        self.work_out = worklog.work_out
        self.presented = __is_presented(worklog)
        self.enabled = __is_enabled(worklog)
        db.session.add(self)
        if bool(self.absencelog):
            self.absencelog.deleted = not self.absence_add
            db.session.add(self.absencelog)
        elif self.absence_add:
            absencelog = AbsenceLogService(self.person_id, self.yymm, self.dd)
            db.session.add(absencelog)
        db.session.commit()
        # update_performlog_enabled.delay(self.person_id, self.yymm)
    def delete(self):
        pass
    @classmethod
    def get(cls, id, yymm, dd):
        return cls.query.filter(cls.person_id==id, cls.yymm==yymm, cls.dd==dd).first()
    @classmethod
    def get_or_new(cls, id, yymm, dd):
        result = cls.get(id, yymm, dd)
        if result is None:
            result = cls(person_id=id, yymm=yymm, dd=dd)
        return result
    @classmethod
    def get_date(cls, id, d):
        yymm = d.strftime('%Y%m')
        dd = d.day
        return get(id, yymm, dd)

from flaskr.services.worklogs import WorkLogService
