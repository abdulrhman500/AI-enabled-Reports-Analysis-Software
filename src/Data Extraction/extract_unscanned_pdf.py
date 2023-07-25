import re
import string
from PyPDF2 import PdfReader

# The logic will be changed
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
def extract_unscanned_text(file_path)-> string:
    reader = PdfReader(file_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text
# def is_bold_or_underLined(file_path, phrase)-> bool:
#     pass

def find_bold_or_underlined_string(pdf_file_path, search_string):
    text = extract_text(pdf_file_path)

    for char_info in pdfminer.layout.LAParams(char_margin=2).char_margin_iter(pdf_file_path):
        text_line, char_bbox, _ = char_info
        char_text = text_line.get_text()

        if search_string in char_text:
            font_state = text_line.dfont
            is_bold = font_state and font_state[1] >= 700
            is_underlined = text_line.underline

            if is_bold or is_underlined:
                start_index = text.find(search_string, char_bbox[0])
                return start_index, is_bold, is_underlined

    return None

def count_occurance(file_path, phrase) -> int:
    pass

def get_text(file_path)->string:
    extracted_text = extract_unscanned_text(file_path)
    start_position = getStartPosition(extracted_text)
    end_position = getEndPosition(extracted_text)
    tasks_text = extracted_text[start_position:end_position]
    return tasks_text