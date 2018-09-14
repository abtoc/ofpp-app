from wtforms import ValidationError
from wtforms.validators import Regexp

class WorkTime(Regexp):
    def __init__(self, *args, **kwargs):
        if 'message' not in kwargs:
            kwargs['message'] = 'HH:MMの形式で入力してください'
        if 'regex' not in kwargs:
            kwargs['regex'] = '^[0-2][0-9]:[0-5][0-9]$'
        super().__init__(*args, **kwargs)

