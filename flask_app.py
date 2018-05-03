from flask import render_template, Flask

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


@web_app.route('/summary')
def page_forex_index():
    return render_template('executive_summary.html', **kwargs, **lfas.key_values())


if __name__ == '__main__':
    web_app.run(host='localhost', port=9000)
