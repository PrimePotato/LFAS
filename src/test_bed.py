from src.lfa_scraper import LfaScraper

lfas = LfaScraper('/Users/EmRo/Documents/LFAS/test_text.txt')

replace_tuples = [
    ('facilities', [
        ('Total Facility A Commitments', 'total_fac_a'),
        ('Total Facility B Commitments', 'total_fac_b'),
        ('Total Facility C Commitments', 'total_fac_c')
    ]),
    ('facilities', [('Total Facility A Commitments', 'total_fac_a')])
]

print('Total Facilities A is {} and B is {}'.format(lfas.get_value('total_fac_a'), lfas.get_value('total_fac_b')))



