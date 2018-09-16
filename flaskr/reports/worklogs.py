from datetime import date
from dateutil.relativedelta import relativedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.platypus import Table
from flaskr.reports import Report
from flaskr.services.worklogs import WorkLogService
from flaskr.helpers import weeka
from flaskr.models import Person, Option

class WorkLogReport(Report):
    def __init__(self, id, yymm):
        super().__init__()
        self.id = id
        self.person = Person.query.get(id)
        self.yymm = yymm
        self.yy = int(yymm[:4])
        self.mm = int(yymm[4:])
    def __call__(self, output):
        psize = portrait(A4)
        super().__call__(output, psize)
    def make_head(self):
        head = {}
        head['ym'] = '{}年{}月'.format(self.yy,self.mm)
        head['name'] = self.person.name
        return head
    def make_items(self):
        foot = dict(
            count = 0,
            value = 0.0,
            break_t = 0.0,
            over_t = 0.0,
            absence = 0,
            late = 0,
            leave = 0
        )
        first = date(self.yy, self.mm, 1)
        items = []
        for dd in range(1, 32):
            if first.month != self.mm:
                items.append(None)
                continue
            log = WorkLogService.get_or_new(self.id, self.yymm, dd)
            item = dict(
                dd = dd,
                ww = weeka(log.date),
                work_in = '',
                work_out = '',
                break_t = '',
                value = '',
                over_t = '',
                absence = '',
                leave = '',
                late = '',
                remarks = ''
            )
            item['work_in'] = log.work_in if bool(log.work_in) else ''
            item['work_out'] = log.work_out if bool(log.work_out) else ''
            if log.break_t is not None:
                item['break_t'] = log.break_t
                foot['break_t'] +=  log.break_t
            if log.value is not None:
                item['value'] = log.value
                foot['value'] += log.value
            if log.presented:
                foot['count'] += 1
            if log.over_t is not None:
                item['over_t'] = log.over_t
                foot['over_t'] += log.over_t
            item['absence'] = '○' if bool(log.absence) else ''
            foot['absence'] = foot['absence'] + (1 if bool(log.absence) else 0) 
            item['leave'] = '○' if bool(log.leave) else ''
            foot['leave'] = foot['leave'] + (1 if bool(log.leave) else 0)
            item['late'] = '○' if bool(log.late) else ''
            foot['late'] = foot['late'] + (1 if bool(log.late) else 0)
            item['remarks'] = log.remarks if bool(log.remarks) else ''
            items.append(item)
            first += relativedelta(days=1)
        return items, foot
    def make_page(self, p, head, items, foot):
        xmargin = 15.0 * mm
        # Title
        name = Option.get('office_name',  '')
        colw = (45.5*mm, 20.5*mm, 24.5*mm, 22.5*mm, 30.5*mm, 27.5*mm)
        data = [[head['ym'],'出勤簿','氏名:',head['name'],'所属：',name]]
        table = Table(data, colWidths=colw, rowHeights=8.0*mm)
        table.setStyle([
            ('FONT',   ( 0, 0), ( 1,-1), 'Gothic', 16),
            ('FONT',   ( 2, 0), (-1,-1), 'Gothic', 12),
            ('ALIGN',  ( 0, 0), (-1,-1), 'CENTER'),
            ('ALIGN',  ( 2, 0), ( 2,-1), 'RIGHT'),
            ('ALIGN',  ( 3, 0), ( 3,-1), 'LEFT'),
            ('ALIGN',  ( 4, 0), ( 4,-1), 'RIGHT'),
            ('ALIGN',  ( 5, 0), ( 5,-1), 'LEFT'),
        ])
        table.wrapOn(p, xmargin, 272.0*mm)
        table.drawOn(p, xmargin, 272.0*mm)
        # Detail
        colw = (10.0*mm, 10.0*mm, 16.5*mm, 16.5*mm, 16.5*mm, 20.5*mm, 16.5*mm, 10.5*mm, 10.5*mm, 10.5*mm, 47.0*mm)
        data =[
            ['日','曜日','始業','終業','休憩','時間','残業', '欠勤', '遅刻', '早退', '備考']
        ]
        for item in items:
            row = []
            if item  is not None:
                row.append(item['dd'])
                row.append(item['ww'])
                row.append(item['work_in'])
                row.append(item['work_out'])
                row.append(item['break_t'])
                row.append(item['value'])
                row.append(item['over_t'])
                row.append(item['absence'])
                row.append(item['late'])
                row.append(item['leave'])
                row.append(item['remarks'])
            data.append(row)
        table = Table(data, colWidths=colw, rowHeights=8.0*mm)
        table.setStyle([
            ('FONT',   ( 0, 0), (-1,-1), 'Gothic', 12),
            ('GRID',   ( 0, 0), (-1,-1), 0.5, colors.black),
            ('BOX',    ( 0, 0), (-1,-1), 1.8, colors.black),
            ('VALIGN', ( 0, 0), (-1,-1), 'MIDDLE'),
            ('ALIGN',  ( 0, 0), (-1,-1), 'CENTER'),
            ('ALIGN',  (10, 1), (10,-1), 'LEFT')
        ])
        table.wrapOn(p, xmargin, 16.0*mm)
        table.drawOn(p, xmargin, 16.0*mm)
        # Foot
        colw = (20.0*mm, 33.0*mm, 16.5*mm, 20.5*mm, 16.5*mm, 10.5*mm, 10.5*mm, 10.5*mm, 47.0*mm)
        data =[
            [
                '合計',
                '{}日'.format(foot['count']),
                foot['break_t'],
                foot['value'],
                foot['over_t'], 
                foot['absence'], 
                foot['late'], 
                foot['leave'],
                ''
            ]
        ]
        table = Table(data, colWidths=colw, rowHeights=8.0*mm)
        table.setStyle([
            ('FONT',   ( 0, 0), (-1,-1), 'Gothic', 12),
            ('GRID',   ( 0, 0), (-1,-1), 0.5, colors.black),
            ('BOX',    ( 0, 0), (-1,-1), 1.8, colors.black),
            ('VALIGN', ( 0, 0), (-1,-1), 'MIDDLE'),
            ('ALIGN',  ( 0, 0), (-1,-1), 'CENTER'),
        ])
        table.wrapOn(p, xmargin, 7.0*mm)
        table.drawOn(p, xmargin, 7.0*mm)
        # Print
        p.showPage()
    def make_report(self, p):
        head = self.make_head()
        items, foot = self.make_items()
        self.make_page(p, head, items, foot)
       
