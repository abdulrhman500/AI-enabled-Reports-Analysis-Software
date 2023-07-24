from PyPDF2 import PdfReader
import re

def getStartPosition(extracted_text):
    start_position = -1
    tasks_pattern = r'\bInternship\s+Performed\s+Tasks\b'
    tasks_match = re.search(tasks_pattern, extracted_text, re.IGNORECASE | re.DOTALL)

    if tasks_match:
        start_position = tasks_match.end()
    
    return start_position

def getEndPosition(extracted_text):
    header_text ="Internship Evaluation"
    end_position = -1
    end_pattern = r'\bInternship\s+Evaluation\b'
    end_match = re.search(end_pattern, extracted_text, re.IGNORECASE | re.DOTALL)
    if end_match:
        end_position = end_match.end() - len(header_text)

    return end_position


def getTextFromFile(path):
    reader = PdfReader(path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    
    start_position = getStartPosition(extracted_text)
    end_position = getEndPosition(extracted_text)
    text_after_tasks = extracted_text[start_position:end_position]

    return text_after_tasks

pdf_file_path = "Ahmed Abdelazeem Omar 40-13742 - Ahmad Kholy.pdf"
extracted_text = getTextFromFile(pdf_file_path)
print(extracted_text)
