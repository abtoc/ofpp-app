from datetime import date

class date_x:
    @classmethod
    def yymm_dd(cls, yymm, dd):
        yy = int(yymm[:4])
        mm = int(yymm[4:])
        dd = int(dd)
        return date(yy, mm, dd)

