import re
from io import BytesIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

RE_DATE = r'\d{2}/\d{2}/\d{4}'
RE_PATTERN = rf'(\w+.*?) \(({RE_DATE})-({RE_DATE}); (.*?)\)\.'


def pdf_to_text(path):
    manager = PDFResourceManager()
    retstr = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    filepath.close()
    device.close()
    retstr.close()
    return text


def parse_text(text):
    titles = ('First Name', 'Last Name', 'Skills', 'About', 'Experience')
    lines = text.split('\n')

    clean_lines = list()
    for j, title in enumerate(titles):
        for i, line in enumerate(lines):
            if line.startswith(title + ':'):
                start = i
            if j == len(titles) - 1:
                end = None
                continue
            if line.startswith(titles[j + 1] + ':'):
                end = i
        clean_lines.append(''.join(lines[start:end]).replace(title + ':', '').strip())

    first_name, last_name, skills, about, experience = clean_lines
    skills = [skill.strip() for skill in skills.split(',')]

    companies = list()

    match = re.findall(RE_PATTERN, experience)
    if match:
        for m in match:
            companies.append(m)
