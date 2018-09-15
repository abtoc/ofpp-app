from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import Table
from flaskr.reports import Report
from flaskr.models import AbsenceLog
class AbsenceLogReport(Report):
    MAX_ROW_COUNT=14
    def __init__(self, yymm):
        super().__init__()
        self.yymm = yymm
        self.yy = int(yymm[:4])
        self.mm = int(yymm[4:])
    def __call__(self, output):
        psize = landscape(A4)
        super().__call__(output, psize)
    def make_page(self, p, items):
        p.setFont('Gothic', 16)
        p.drawString(110.0*mm, 180.0*mm, '欠席時対応加算記録')
        p.setFont('Gothic', 9)
        p.drawString(105.0*mm, 174.0*mm, '※利用を中止した日の前々日、前日または当日に連絡があった場合に利用者の状況を確認し、その内容を記録する。')
        colw = (18.0*mm, 18.0*mm, 23.5*mm, 23.5*mm, 35.0*mm, 148*mm)
        data = [['利用予定日','連絡日','連絡者','対応職員','欠席理由','相談援助']]
        count = 0
        while count < len(items):
            item = [
                items[count].date,
                items[count].contact,
                items[count].person.name,
                items[count].staff.name if items[count].staff else '',
                items[count].reason,
                items[count].remarks
            ]
            data.append(item)
            count = count + 1
        while self.MAX_ROW_COUNT > count:
            data.append([])
            count = count + 1
        table = Table(data, colWidths=colw, rowHeights=10.0*mm)
        table.setStyle([
            ('FONT',   ( 0, 0), (-1,-1), 'Gothic', 9),
            ('GRID',   ( 0, 0), (-1,-1), 0.5, colors.black),
            ('BOX',    ( 0, 0), (-1,-1), 1.8, colors.black),
            ('VALIGN', ( 0, 0), (-1,-1), 'MIDDLE'),
            ('ALIGN',  ( 0, 0), (-1,-1), 'CENTER'),
            ('ALIGN',  ( 5, 1), ( 5,-1), 'LEFT'),
        ])
        table.wrapOn(p, 18.0*mm, 20.0*mm)
        table.drawOn(p, 18.0*mm, 20.0*mm)
        p.showPage()
    def make_report(self, p):
        logs = AbsenceLog.query.filter(
            AbsenceLog.yymm == self.yymm,
        ).order_by(
            AbsenceLog.yymm,
            AbsenceLog.dd
        ).all()
        print(logs)
        count = len(logs)
        pos = 0
        while count > pos:
            items = logs[pos:pos+self.MAX_ROW_COUNT]
            self.make_page(p, items)
            pos += self.MAX_ROW_COUNT
