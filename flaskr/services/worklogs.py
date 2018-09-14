from flaskr import db
from flaskr.models import WorkLog
from flaskr.services.performlogs import PerformLogService

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
    def update_no_staff(self, form):
        form.populate_obj(self)
        if not bool(self.remarks):
            self.remarks = None
        if self.value is not None:
            self.presented = True
        else:
            self.presented = False
        db.session.add(self)
        db.session.commit()
    def update_api(self, tm):
        hhmm = tm.strftime('%H:%M')
        if bool(self.work_in):
            self.work_in = hhmm
        else:
            self.work_out = hhmm
            self.value = None
        self.presented = True
        self.absence = False
        db.session.add(self)
        db.session.commit()
        # update_worklog_value.delay(self.person_id, self.yymm, self.dd)
        performlog = PerformLogService.get_or_new(self.person_id, self.yymm, self.dd)
        performlog.updte_worklog(self)
    def update_performlog(performlog):
        self.work_in = performlog.work_in
        self.work_out = performlog.work_out
        self.absence = performlog.absence
        self.presented = bool(self.work_in) or bool(self.work_out)
        db.session.add(self)
        db.session.commit()
        # update_worklog_value.delay(self.person_id, self.yymm, self.dd)
    def delete(self):
        if not self.person.staff:
            raise ValueError('利用者は実績登録から削除してください')
        db.session.delete(self)
        db.session.commit()
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
