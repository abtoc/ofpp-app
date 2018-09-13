from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, ValidationError
from wtforms.validators import Required
import json
import jsonschema

class TimeRuleForm(FlaskForm):
    caption = StringField('題名', validators=[Required(message='入力必須です')])
    rules = TextAreaField('タイムテーブル', render_kw={'rows': 16})
    def validate_rule(form, field):
        if len(field) == 0:
            raise ValidationError('入力必須です')
        try:
            data = json.loads(field.data)
            jsonschema.validate(data, schema)
        except Exception as e:
            raise ValidationError(e)

schema = {
  "type": "object",
  "title": "Root",
  "required": [ "times", "core" ],
  "properties": {
    "max": { "type": "number", "title":  "最大勤務時間" },
    "times": {
      "type": "array",
      "title": "The Times Schema",
      "items": {
        "type": "object",
        "title": "タイムテーブル",
        "required": [ "caption", "start", "end", "in", "out", "value" ],
        "properties": {
          "caption": { "type": "string", "title": "Caption", "pattern": "^(.*)$"  },
          "start": { "type": "string", "title": "開始時刻", "pattern": "^(.*)$" },
          "end": { "type": "string", "title": "終了時刻", "pattern": "^(.*)$"  },
          "in": { "type": "boolean", "title": "開始時有効" },
          "out": { "type": "boolean", "title": "終了時有効" },
          "value": { "type": "number", "title": "時刻値" }
        }
      }
    },
    "core": {
      "type": "object",
      "title": "コアタイム",
      "required": [ "start", "end", "value" ],
      "properties": {
        "start": { "type": "number", "title": "開始時刻値" },
        "end": { "type": "number", "title": "終了時刻値" },
        "value": { "type": "number", "title": "勤務時間" }
      }
    },
    "break": {
      "type": "array",
      "title": "The 休憩時刻 Schema",
      "items": {
        "type": "object",
        "title": "休憩時刻",
        "required": [ "start", "end", "value" ],
        "properties": {
          "start": { "type": "number", "title": "開始時刻値" },
          "end": { "type": "number", "title": "終了時刻値"  },
          "value": { "type": "number", "title": "休憩時間"  }
        }
      }
    }
  }
}
