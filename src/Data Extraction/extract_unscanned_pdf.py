import re
import string
from PyPDF2 import PdfReader

# The logic will be changed
def getStartPosition(extracted_text):
    start_position = -1
    tasks_pattern = r'\bInternship\s+Performed\s+Tasks\b'
    tasks_match = re.search(tasks_pattern, extracted_text, re.IGNORECASE | re.DOTALL)
    print(tasks_match)
    if tasks_match:
        start_position = tasks_match.end()
    
    return start_position

def getEndPosition(extracted_text):
    header_text ="Internship Evaluation"
    end_position = -1
    end_pattern = r'\bInternship\s+Evaluation\b'
    end_match = re.search(end_pattern, extracted_text, re.IGNORECASE | re.DOTALL)
    print(end_match)
    if end_match:
        end_position = end_match.end() - len(header_text)

    return end_position
def extract_unscanned_text(file_path)-> string:
    reader = PdfReader(file_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text

def get_text(file_path)->string:
    extracted_text = extract_unscanned_text(file_path)
    start_position = getStartPosition(extracted_text)
    end_position = getEndPosition(extracted_text)
    tasks_text = extracted_text[start_position:end_position]
    print(tasks_text)
    return tasks_text

if __name__ == "__main__":
    pdf_file_path = "C:\\Users\\hoda2\\Documents\\NLP Internship\\Dirty Files\\correct template\\(A) 1-merged - Rawan Ahmad.pdf"
    get_text(pdf_file_path)
    # print(get_text)