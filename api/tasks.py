import re
import logging
from io import BytesIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from .models import CV, Experience, Company, Skill
from resume.celeryconfig import celery_app


RE_DATE = r'\d{4}-\d{2}-\d{2}'
RE_PATTERN = rf'(\w+.*?) \(({RE_DATE}) - ({RE_DATE}); (.*?)\)\.'

api_logger = logging.getLogger('api')


@celery_app.task(name='pdf_to_text')
def pdf_to_text(path=None):
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

    api_logger.info(f"{path} was successfully converted to text")
    parse_text.delay(text.decode())


@celery_app.task(name='parse_text')
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

    insert_data.delay(first_name, last_name, skills, about, companies)


@celery_app.task(name='insert_data')
def insert_data(first_name, last_name, skills, about, companies):
    cv, created = CV.objects.update_or_create(first_name=first_name, last_name=last_name, defaults={'about': about})
    api_logger.debug(f"New CV ({cv}) was created: {created}")

    for skill in skills:
        skill_obj, _ = Skill.objects.get_or_create(name=skill)
        cv.skill.add(skill_obj)
        cv.save()

    for company in companies:  # company = ('Company Name', '2015-01-11', '2018-07-26', 'Description') - example
        company_obj, _ = Company.objects.get_or_create(name=company[0])
        Experience.objects.update_or_create(company=company_obj, resume=cv,
                                            defaults={'date_start': company[1], 'date_end': company[2],
                                                      'description': company[3]})
