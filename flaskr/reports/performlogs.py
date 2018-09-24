from dateutil.relativedelta import relativedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.platypus import Table
from sqlalchemy import func
from flaskr import db
from flaskr.reports import Report
from flaskr.services.performlogs import PerformLogService
from flaskr.helpers import weeka
from flaskr.models import Person, PerformLog, Recipient, Option

class PerformLogReport(Report):
    def __init__(self, id, yymm):
        super().__init__()
        self.id = id
        self.person = Person.query.get(id)
        self.recipient = Recipient.query.get(id)
        self.yymm = yymm
        self.yy = int(yymm[:4])
        self.mm = int(yymm[4:])
        if self.mm <= 3:
            self.yymm1 = str(self.yy - 1) + '04'
        else:
            self.yymm1 = str(self.yy) + '04'
    def __call__(self, output):
        psize = portrait(A4)
        super().__call__(output, psize)
    def make_head(self):
        gg = self.yy - 1988
        head = {}
        head['gm'] = '平成{}年{}月分'.format(gg,self.mm)
        head['name'] = self.person.name
        head['idm'] = self.person.idm
        head['number'] = self.recipient.number
        head['amount'] = self.recipient.amount
        head['usestart'] = ''
        head['usestart30d'] = ''
        if bool(self.person.recipient.usestart):
            self.usestart = self.person.recipient.usestart
            self.usestart30d = self.usestart + relativedelta(days=29)
            yy1 = self.usestart.year
            mm1 = self.usestart.month
            yy2 = self.usestart30d.year
            mm2 = self.usestart30d.month
            if ((yy1 == self.yy) and (mm1 == self.mm)) or ((yy2 == self.yy) and (mm2 == self.mm)):
                head['usestart'] = self.usestart
                head['usestart30d'] = self.usestart30d
        else:
            self.usestart = None
            self.usestart30d = None
        return head
    def make_items(self):
        foot = dict(
            count = 0,
            absence = 0,
            pickup = 0,
            visit = 0,
            meal = 0,
            medical = 0,
            experience = 0,
            outside = 0,
            outemp = 0,
            usestart = 0
        )
        logs = PerformLogService.query.filter(
            PerformLog.person_id == self.id,
            PerformLog.yymm == self.yymm
        ).order_by(
            PerformLog.person_id,
            PerformLog.yymm,
            PerformLog.dd
        ).all()
        items = []
        for log in logs:
            if not log.enabled:
                continue
            item = dict(
                dd = log.date.day,
                ww = weeka(log.date),
                stat = '欠席' if log.absence_add else '',
                work_in = '',
                work_out = '',
                pickup_in = '',
                pickup_out = '',
                visit = '',
                meal = '',
                medical = '',
                experience = '',
                outside = '',
                outemp = '',
                remarks = ''
            )
            foot['count'] += 1 if bool(log.presented) else 0
            item['work_in'] = log.work_in if bool(log.work_in) else ''
            item['work_out'] = log.work_out if bool(log.work_out) else ''
            item['pickup_in'] = 1 if bool(log.pickup_in) else ''
            item['pickup_out'] = 1 if bool(log.pickup_out) else ''
            item['visit'] = log.visit
            item['meal'] = 1 if bool(log.meal) else ''
            item['medical'] = log.medical
            item['experience'] = log.experience
            item['outside'] = 1 if bool(log.outside) else ''
            item['outemp'] = 1 if bool(log.outemp) else ''
            foot['pickup'] += 1 if bool(log.pickup_in) else 0
            foot['pickup'] += 1 if bool(log.pickup_out) else 0
            foot['visit'] += 1 if bool(log.visit) else 0
            foot['meal'] += 1 if bool(log.meal) else 0
            foot['medical'] += 1 if bool(log.medical) else 0
            foot['experience'] += 1 if bool(log.experience) else 0
            foot['outside'] += 1 if bool(log.outside) else 0
            foot['outemp'] += 1 if bool(log.outemp) else 0
            if bool(self.usestart) and (log.presented):
                foot['usestart'] += 1 if (log.date >= self.usestart) and (log.date <= self.usestart30d) else 0
            item['remarks'] = log.remarks
            items.append(item)
        q = db.session.query(
            func.count(PerformLog.outside)
        ).filter(
            PerformLog.person_id == self.id,
            PerformLog.yymm >= self.yymm1,
            PerformLog.yymm <= self.yymm,
            PerformLog.outside == True
        ).first()
        foot['outside_sum'] = q[0] if bool(q) else 0
        return items, foot
    def make_page(self, p, head, items, foot):
        xmargin = 15.0 * mm
        # Title
        p.setFont('Gothic', 16)
        p.drawString(75*mm, 275*mm, '就労継続支援提供実績記録票')
        p.setFont('Gothic', 11)
        p.drawString(17*mm, 275*mm, head['gm'])
        # Header
        colw = (25.0*mm, 29.5*mm, 32.0*mm, 32.0*mm, 22.0*mm, 43.5*mm)
        idm = head['idm']
        number = Option.get('office_number','')
        name = Option.get('office_name',  '')
        data =[
            ['受給者証番号',head['number'],'支給決定障害者氏名',head['name'],'事業所番号',number],
            ['契約支給量',head['amount'],'','','事業者及び\nその事業所',name]
        ]
        table = Table(data, colWidths=colw, rowHeights=10.0*mm)
        table.setStyle([
            ('FONT',   ( 0, 0), (-1,-1), 'Gothic', 8),
            ('GRID',   ( 0, 0), (-1,-1), 0.5, colors.black),
            ('BOX',    ( 0, 0), (-1,-1), 1.8, colors.black),
            ('VALIGN', ( 0, 0), (-1,-1), 'MIDDLE'),
            ('ALIGN',  ( 0, 0), (-1,-1), 'CENTER'),
            ('ALIGN',  ( 1, 1), ( 1, 1), 'LEFT'),
            ('SPAN',   ( 1, 1), ( 3, 1))
        ])
        table.wrapOn(p, xmargin, 252.0*mm)
        table.drawOn(p, xmargin, 252.0*mm)
        # Detail
        colw = (8.6*mm,11.0*mm, 17.2*mm, 17.2*mm,  17.2*mm, 6.0*mm, 6.0*mm, 9.6*mm, 6.6*mm, 6.6*mm, 6.6*mm, 8.6*mm, 8.6*mm, 14.6*mm, 39.6*mm)
        data = [
            ['日\n付', '曜\n日','サービス提供実績',    '', '' , '',  '',  '', '', '', '', '','', '利用者\n確認印', '備考'],
            ['',       '',      'サービス提供\nの状況','開始時間', '終了時間', '送迎加算', '',   '訪問支援\n特別加算', '食事\n提供\n加算', '医療\n連携\n体制\n加算', '体験\n利用\n支援\n加算', '施設外\n就労', '施設外\n支援'], 
            ['',       '',      '',                    '',         '',         '往', '復', '時間数'           ]       
        ]
        count = 0
        for item in items:
            row = []
            row.append(item['dd'])
            row.append(item['ww'])
            row.append(item['stat'])
            row.append(item['work_in'])
            row.append(item['work_out'])
            row.append(item['pickup_in'])
            row.append(item['pickup_out'])
            row.append(item['visit'])
            row.append(item['meal'])
            row.append(item['medical'])
            row.append(item['experience'])
            row.append(item['outemp'])
            row.append(item['outside'])
            row.append('')
            row.append(item['remarks'])
            data.append(row)
            count = count + 1
        while count < 28:
            data.append([])
            count = count + 1
        table = Table(data, colWidths=colw, rowHeights=7.0*mm)
        table.setStyle([
            ('FONT',   ( 0, 0), (-1,-1), 'Gothic', 9),
            ('FONT',   ( 2, 1), ( 2, 1), 'Gothic', 7), # サービス提供の状況
            ('FONT',   ( 5, 1), ( 6, 1), 'Gothic', 7), # 送迎加算
            ('FONT',   ( 7, 1), ( 7, 1), 'Gothic', 5), # 訪問支援特別加算
            ('FONT',   ( 7, 2), ( 7, 2), 'Gothic', 7), # 訪問支援特別加算
            ('FONT',   ( 8, 1), ( 8, 1), 'Gothic', 7), # 食事提供加算
            ('FONT',   ( 9, 1), ( 9, 1), 'Gothic', 6), # 医療連携体制加算
            ('FONT',   (10, 1), (10, 1), 'Gothic', 6), # 体験利用加算
            ('FONT',   (11, 1), (11, 1), 'Gothic', 7), # 施設外就労
            ('FONT',   (12, 1), (12, 1), 'Gothic', 7),
            ('GRID',   ( 0, 0), (-1,-1), 0.5, colors.black),
            ('BOX',    ( 0, 0), (-1,-1), 1.8, colors.black),
            ('VALIGN', ( 0, 0), (-1,-1), 'MIDDLE'),
            ('ALIGN',  ( 0, 0), (-1,-1), 'CENTER'),
            ('SPAN',   ( 0, 0), ( 0, 2)), # 日付
            ('SPAN',   ( 1, 0), ( 1, 2)), # 曜日
            ('SPAN',   ( 2, 0), (12, 0)), # サービス提供実績
            ('SPAN',   (13, 0), (13, 2)), # 利用者確認印
            ('SPAN',   (14, 0), (14, 2)), # 備考
            ('SPAN',   ( 2, 1), ( 2, 2)), # サービス提供の状況
            ('SPAN',   ( 3, 1), ( 3, 2)), # 開始時間
            ('SPAN',   ( 4, 1), ( 4, 2)), # 終了時間
            ('SPAN',   ( 5, 1), ( 6, 1)), # 送迎加算
            ('SPAN',   ( 8, 1), ( 8, 2)), # 食事提供加算
            ('SPAN',   ( 9, 1), ( 9, 2)), # 医療連携体制加算
            ('SPAN',   (10, 1), (10, 2)), # 体験利用支援加算
            ('SPAN',   (11, 1), (11, 2)), # 施設外就労
            ('SPAN',   (12, 1), (12, 2)), # 施設外支援
            ('ALIGN',  (14, 3), (14,-1), 'LEFT'),
        ])
        table.wrapOn(p, xmargin, 32.0*mm)
        table.drawOn(p, xmargin, 32.0*mm)
        # Footer
        colw = (36.8*mm, 34.2*mm, 12.0*mm, 9.6*mm, 6.6*mm, 6.6*mm, 6.6*mm, 8.6*mm, 13.6*mm, 10.0*mm, 26.2*mm, 13.2*mm)
        data = [
            [
                '合計', 
                '{}回'.format(foot['count']),
                '{}回'.format(foot['pickup']),
                '{}回'.format(foot['visit']),
                '{}回'.format(foot['meal']),
                '{}回'.format(foot['medical']),
                '{}回'.format(foot['experience']),
                '{}回'.format(foot['outemp']),
                '施設外\n支援',
                '当月',
                '{}日      '.format(foot['outside']),
                ''
            ],
            ['', '', '', '', '', '', '', '', '', '累計',
                '{}日/180日'.format(foot['outside_sum'])
            ]
        ]
        table = Table(data, colWidths=colw, rowHeights=4.0*mm)
        table.setStyle([
            ('FONT',   ( 0, 0), (-1,-1), 'Gothic', 8),
            ('FONT',   ( 0, 0), ( 0, 0), 'Gothic', 9),
            ('GRID',   ( 0, 0), (-1,-1), 0.5, colors.black),
            ('BOX',    ( 0, 0), (-1,-1), 1.8, colors.black),
            ('VALIGN', ( 0, 0), (-1,-1), 'MIDDLE'),
            ('ALIGN',  ( 0, 0), (-1,-1), 'CENTER'),
            ('ALIGN',  (10, 0), (10,-1), 'RIGHT'),
            ('SPAN',   ( 0, 0), ( 0, 1)), # 合計
            ('SPAN',   ( 1, 0), ( 1, 1)), # 利用回数
            ('SPAN',   ( 2, 0), ( 2, 1)), # 送迎加算
            ('SPAN',   ( 3, 0), ( 3, 1)), # 訪問支援特別加算
            ('SPAN',   ( 4, 0), ( 4, 1)), # 食事提供加算
            ('SPAN',   ( 5, 0), ( 5, 1)), # 医療連携体制加算
            ('SPAN',   ( 6, 0), ( 6, 1)), # 体験利用支援加算
            ('SPAN',   ( 7, 0), ( 7, 1)), # 施設外就労
            ('SPAN',   ( 8, 0), ( 8, 1)), # 施設外支援
            ('SPAN',   (11, 0), (11, 1)), 
        ])
        table.wrapOn(p, xmargin, 23.2*mm)
        table.drawOn(p, xmargin, 23.2*mm)
        # UseStart
        colw=(28.0*mm,21.5*mm,30.5*mm,21.5*mm,30.5*mm,21.5*mm,30.5*mm)
        data=[
            ['初期加算','利用開始日',head['usestart'],'30日目',head['usestart30d'],'当月算定日数','{}日'.format(foot['usestart'])]
        ]
        table = Table(data, colWidths=colw, rowHeights=6.5*mm)
        table.setStyle([
            ('FONT',   ( 0, 0), (-1,-1), 'Gothic', 9),
            ('GRID',   ( 0, 0), (-1,-1), 0.5, colors.black),
            ('BOX',    ( 0, 0), (-1,-1), 1.8, colors.black),
            ('VALIGN', ( 0, 0), (-1,-1), 'MIDDLE'),
            ('ALIGN',  ( 0, 0), (-1,-1), 'CENTER')
        ])
        table.wrapOn(p, xmargin, 15.0*mm)
        table.drawOn(p, xmargin, 15.0*mm)
        # IDm
        p.setFont('Gothic', 11)
        p.drawString(17*mm, 10*mm, '記録ICカード：{idm}'.format(idm=idm))
        # Print
        p.showPage()
    def make_report(self, p):
        head = self.make_head()
        items, foot = self.make_items()
        self.make_page(p, head, items, foot)
