import re

from flask import render_template, Flask
from jinja2 import evalcontextfilter, escape, Markup

from src.lfa_scraper import LfaScraper

lfas = LfaScraper('data/test_text.txt')

kwargs = {
    'financial_covenant_dets': [
        ['Cashflow Cover', 'Senior Interest Cover'],
        ['Interest Cover', 'Senior Adjusted Leverage'],
        ['Capital Expenditure', 'Adjusted Leverage'],
    ]
}

web_app = Flask(__name__)

print(lfas.key_values())

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


@web_app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@web_app.route('/summary')
def page_forex_index():
    return render_template('executive_summary.html', **kwargs, **lfas.key_values())


if __name__ == '__main__':
    web_app.run(host='localhost', port=9000)
