from flask import abort
from flaskr import db
from flaskr.models import TimeRule
import json

class TimeRuleService:
    def __init__(self, id):
        self.item = TimeRule.get(id)
    def calc(self, work_in, work_out):
        if (not bool(work_in)) or (not bool(work_out)):
            return None, None, None, None, None
        rules = json.loads(self.item.rules)
        w_in = rules['core']['start']
        w_out = rules['core']['end']
        for i in rules['times']:
            if i['in'] and (i['start'] <= work_in) and (work_in < i['end']):
                w_in = i['value']
                break
        for i in rules['times']:
            if i['out'] and (i['start'] <= work_out) and (work_out < i['end']):
                w_out = i['value']
                break
        value = w_out - w_in
        break_t = 0.0
        if 'break' in rules:
            for i in rules['break']:
                if (w_in <= i['start']) and (w_out >= i['end']):
                    break_t += i['value']
        value -= break_t
        if value < 0:
            value = 0.0
        elif ('max' in rules) and (value >= rules['max']):
            value = rules['max']
        over_t = 0.0
        if value > rules['core']['value']:
            over_t = value - rules['core']['value']
        return value, break_t, over_t, w_in > rules['core']['start'], w_out < rules['core']['end']

