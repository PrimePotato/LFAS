from lfa_scraper import LfaScraper

lfas = LfaScraper('/Users/EmRo/Documents/LFAS/test_text.txt')

replace_tuples = [
    ('facilities', [
        ('Total Facility A Commitments', 'total_fac_a'),
        ('Total Facility B Commitments', 'total_fac_b'),
        ('Total Facility C Commitments', 'total_fac_c')
    ]),
    ('facilities', [('Total Facility A Commitments', 'total_fac_a')])
]

# print(lfas.get_value('facilities'))
print('Total Facilities A is {} and B is {}'.format(lfas.get_value('total_fac_a'),lfas.get_value('total_fac_b')))

# for section, rep_list in replace_tuples:
#     txt = lfas.get_value(section)
#     for name, var_name in rep_list:
#         txt = txt.replace(name, lfas.get_value(var_name))
#     print(txt)
