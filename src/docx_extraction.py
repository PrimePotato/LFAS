
import docx


doc = docx.Document(r'D:\per_projects\LFAS\data\template_docx.docx')
tables = doc.tables
for table in tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                print(paragraph.text)
