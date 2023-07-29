#### Prerequisites:
# pip install PyMuPDF
# pip install pytesseract
# pip install pdf2image

# Install poppler:
# 1. Download the latest version from: https://github.com/oschwartz10612/poppler-windows/releases 
# 2. Extract the zip file to a folder
# 3. Add the path to the /bin folder to the PATH environment variable
# 4. Restart VS Code (or your IDE)


import fitz
import re
import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def is_bold(font_flags):
    return bool(font_flags & (1 << 4))

def extract_bold_text_with_regex(pdf_file_path, regex_pattern):
    count = 0
    count_list = []
    bold_text_with_regex = []
    doc = fitz.open(pdf_file_path)
    
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        blocks = page.get_text("dict", flags=11)["blocks"]
        
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    if re.search(regex_pattern, span["text"]):
                        count += 1
                        if is_bold(span["flags"]):
                            count_list.append(count)
                            bold_text_with_regex.append(span["text"])
    
    doc.close()
    return bold_text_with_regex, count_list, count

# Function to check if the PDF is scanned (contains images)
def is_scanned_pdf(pdf_path, start_page, end_page=None, max_words_threshold=50):
    try:
        with fitz.open(pdf_path) as doc:
            if end_page is None:
                end_page = doc.page_count

            for page_number in range(start_page, end_page):
                page = doc.load_page(page_number)
                text = page.get_text()

                # Count the number of words in the page
                num_words = len(text.split())

                # If the number of words is below the threshold, consider it as a scanned page
                if num_words <= max_words_threshold:
                    return True

            return False

    except Exception as e:
        print(f"Error checking if PDF is scanned: {e}")
        return False

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

# Function to extract a section from the OCR text
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



# Main Function
if __name__ == "__main__":
    pdf_file_path = "path/to/pdf.pdf"

    # Check if the PDF is scanned
    start_page = 4 # Change this to the page number you want to start from

    if is_scanned_pdf(pdf_file_path, start_page, end_page=None):
        print("The PDF is scanned")
        # Extract section from the OCR text
        ocr_text = pdf_to_text(pdf_file_path, start_page)
        section_title = "Internship Performed Tasks"
        section_content = extract_section_ocr(ocr_text, section_title)
        print(f"{section_title}:\n{section_content}")

    else:
        print("The PDF is not scanned")
        regex_pattern = "" 
        bold_text_list_with_string, count_list, count = extract_bold_text_with_regex(pdf_file_path, regex_pattern)
        print(count)
        print(count_list)

        boldd = None
        bold2 = None
        flag = False
        for bold_text in bold_text_list_with_string:
            print(f"Bold Text: {str(bold_text).strip()}")
        
        for bold_text in bold_text_list_with_string:

            if flag and bold2 is None:
                bold2 = str(bold_text).strip()
                break

            if not flag:
                bold_words = str(bold_text).strip().split()
            if any(word.lower().startswith("task") for word in bold_words):
                boldd = str(bold_text).strip()
                flag = True


        print("Bold Text containing 'Tasks':", boldd)
        print("Next Bold Text:", bold2)


        # print(str(bold_text).strip().split())

def extract_text_from_headline(pdf_path, boldd):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()

        start_index = full_text.lower().find(boldd.lower())
        end_index = full_text.lower().find(bold2.lower())

        if start_index != -1:
            extracted_text = full_text[start_index:end_index]
            return extracted_text
        else:
            return None

extracted_text = extract_text_from_headline(pdf_file_path, boldd)
if extracted_text:
    print(extracted_text)
else:
    print("Headline not found in the PDF.")



