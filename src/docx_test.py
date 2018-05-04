# from __future__ import (
#     absolute_import, division, print_function, unicode_literals
# )
from collections import Counter
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


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


def iter_headings(paragraphs):
    for paragraph in paragraphs:
        if paragraph.style.name.startswith('Heading'):
            yield paragraph


def number_headings(doc):
    cnt = Counter()
    num_map_para = {}
    hdr_num = '0.0.0'
    num_map_para[hdr_num] = []
    for para in iter_block_items(document):
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

document = Document(r'D:\per_projects\LFAS\data\template_docx.docx')
# for block in iter_block_items(document):
#     # print(block.text if isinstance(block, Paragraph) else '<table>')
#     print(block if isinstance(block, Table) else '<table>')

nh = number_headings(document)

print(nh)
