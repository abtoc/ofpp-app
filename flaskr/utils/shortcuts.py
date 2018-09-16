from flask import abort

class ModelMixInID(object):
    @classmethod
    def get(cls, id):
        return cls.query.get(id)
    @classmethod
    def get_or_404(cls, id):
        result = cls.get(id)
        if result is None:
            abort(404)
        return result

class ModelMixInYYMMDD(object):
    @classmethod
    def get_or_new(cls, id, yymm, dd):
        result = cls.query.get((id, yymm, dd))
        if result is None:
            result = cls(person_id=id, yymm=yymm, dd=dd)
        return result
    @classmethod
    def get_date(cls, id, date):
        yymm = date.strftime('%Y%m')
        dd = date.day
        return cls.query.get((id, yymm, dd))
