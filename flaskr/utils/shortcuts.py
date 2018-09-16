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

