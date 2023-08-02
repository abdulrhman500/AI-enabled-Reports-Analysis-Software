import fitz
import re
import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import constants
def pdf_to_text(pdf_path, start_page=1):
    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    text = ""
    for page_num, image in enumerate(images, start=1):
        if page_num < start_page:
            continue

        # Perform OCR on the image to extract text
        extracted_text = pytesseract.image_to_string(image, lang='eng')
        text += f"Page {page_num}:\n{extracted_text}\n"

    return text

def extract_section_ocr(text, section_title):
    section_found = False
    section_content = ""

    # Split the OCR text into lines
    lines = text.split('\n')

    for line in lines:
        # Check if the line contains the section title
        if section_title.lower() in line.lower():
            section_found = True

            # Capture the text after the section title until the next section or end of the document
            section_content += re.sub(rf'^.*{re.escape(section_title)}\s*:', '', line.strip()) + " "
        elif section_found:
            # Extract content until the next section or end of the document
            if line.strip():
                section_content += line.strip() + " "
            else:
                break

    return section_content.strip()

def get_text(pdf_file_path,start_page=4):
    ocr_text = pdf_to_text(pdf_file_path, start_page)
    section_title = constants.TASKS_SECTION_HEADLINE
    section_content = extract_section_ocr(ocr_text, section_title)
    # print(f"{section_title}:\n{section_content}")