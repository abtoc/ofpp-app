from datetime import date

class date_x:
    def __init__(self, adate=date.today()):
        self.__date = adate
    def __add__(self, obj):
        return date_x(self.__date + obj)
    def __sub__(self, obj):
        return date_x(self.__date - obj)
    def to_yymm_dd(self):
        return self.__date.strftime('%Y%m'), self.__date.strftime('%d')
    @property
    def date(self):
        return self.__date
    @classmethod
    def yymm_dd(cls, yymm, dd):
        yy = int(yymm[:4])
        mm = int(yymm[4:])
        dd = int(dd)
        return date_x(date(yy, mm, dd))

