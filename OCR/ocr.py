# Description: Extract text from a PDF file using OCR

#### Prerequisites:
# Install pytesseract: pip install pytesseract
# Install pdf2image: pip install pdf2image
# Install poppler:
# 1. Download the latest version from: https://github.com/oschwartz10612/poppler-windows/releases 
# 2. Extract the zip file to a folder
# 3. Add the path to the bin folder to the PATH environment variable
# 4. Restart VS Code (or your IDE)


import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import re

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


def extract_section(text, section_title):
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

if __name__ == "__main__":
    ### Change these variables to point to your PDF file and the page number you want to start from
    pdf_path = "C:/Users/maria/OneDrive/Desktop/Internship Project/scanned.pdf"
    start_page = 4  # Change this to the page number you want to start from
    extracted_text = pdf_to_text(pdf_path, start_page)

    # Extract the specific section with the title "Internship Performed Tasks"
    section_title = "Internship Performed Tasks"
    section_content = extract_section(extracted_text, section_title)

    print("Extracted Section Content:")
    print(section_content)

    # Save the extracted section to a text file
    with open("output_section.txt", "w", encoding="utf-8") as section_file:
        section_file.write(section_content)

