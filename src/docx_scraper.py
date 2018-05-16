from collections import Counter

import os
import yaml
import pandas as pd
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from locations import base_location


class DocxScraper(object):
    def __init__(self, doc_location):
        self.doc_location = doc_location
        self.document = Document(doc_location)
        self.num_hdr = self.number_headings(self.document)
        with open(os.path.join(base_location, 'cfg/table_config.yaml')) as stream:
            self.tbl_cfg = yaml.load(stream)
        self.table_data = self._table_data()

    def _table_data(self):
        tbl_dfs = {}
        for table_name, dets in self.tbl_cfg['FinancialCovenants'].items():
            heading_data = self.num_hdr.get(dets['location'])
            tbl = [t for t in heading_data if isinstance(t, Table)][0]
            data_set = []
            for row in tbl.rows:
                row_data = []
                for cell in row.cells:
                    txt = cell.text
                    txt = txt.replace('Column 1\n', '').replace('Column 2\n', '')
                    row_data.append(txt)
                data_set.append(row_data)
            tbl_dfs[table_name] = pd.DataFrame(data_set[1:], columns=data_set[0])
        return tbl_dfs

    @staticmethod
    def iter_block_items(parent):
        if isinstance(parent, _Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        else:
            raise ValueError("something's not right")

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)

    @staticmethod
    def iter_headings(paragraphs):
        for paragraph in paragraphs:
            if paragraph.style.name.startswith('Heading'):
                yield paragraph

    @staticmethod
    def number_headings(doc):
        cnt = Counter()
        num_map_para = {}
        hdr_num = '0.0.0'
        num_map_para[hdr_num] = []
        for para in DocxScraper.iter_block_items(doc):
            hdr_type = para.style.name[-1]
            if para.style.name.startswith('Heading') and int(hdr_type) < 4:
                cnt[hdr_type] += 1
                for i in range(int(hdr_type) + 1, 4):
                    cnt[str(i)] = 0
                str_cnt = [str(c) for c in cnt.values()]
                hdr_num = '.'.join(str_cnt)
                num_map_para[hdr_num] = [para]
            else:
                num_map_para[hdr_num].append(para)
        return num_map_para

    def html_table(self, name):
        return self.table_data[name].to_html(index=False, classes='table table-bordered table-responsive')


if __name__ == "__main__":
    ds = DocxScraper(r'D:\per_projects\LFAS\data\template_docx.docx')
    print(ds.html_table('CashflowCover'))
