from flaskr import app

__WEEK = ('月', '火', '水', '木', '金', '土', '日')

@app.template_filter('weeka')
def weeka(date):
    return __WEEK[date.weekday()] if date is not None else ''

@app.template_filter('strftime')
def strftime(date, format='%Y/%m/%d'):
    if date is None:
        return ''
    return date.strftime(format) if date is not None else ''

@app.template_filter('do_not_show_none')
def do_not_show_none(value):
        return value if value is not None else ''

