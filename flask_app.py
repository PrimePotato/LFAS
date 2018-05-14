import re

import os
from flask import render_template, Flask
from jinja2 import evalcontextfilter, escape, Markup

from locations import base_location
from src.docx_scraper import DocxScraper
from src.lfa_scraper import LfaScraper

web_app = Flask(__name__)

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

lfas = LfaScraper(os.path.join(base_location, 'data/test_text.txt'))
ds = DocxScraper(os.path.join(base_location, 'data/template_docx.docx'))


kwargs = {
    'financial_covenant_dets': [
        [('Cashflow Cover', ds.html_table('CashflowCover')),
         ('Senior Interest Cover', ds.html_table('SeniorInterestCover'))],
        [('Interest Cover', ds.html_table('InterestCover')),
         ('Senior Adjusted Leverage', ds.html_table('SeniorAdjustedLeverage'))],
        [('Capital Expenditure', ds.html_table('CapitalExpenditure')),
         ('Adjusted Leverage', ds.html_table('AdjustedLeverage'))],
    ]
}


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
