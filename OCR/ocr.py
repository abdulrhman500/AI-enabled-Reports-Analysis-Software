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

if __name__ == "__main__":

    ### Change these variables to point to your PDF file and the page number you want to start from
    pdf_path = "path/to/pdf/file.pdf"
    start_page = 4  # Change this to the page number you want to start from
    extracted_text = pdf_to_text(pdf_path, start_page)

    # Save the extracted text to a text file
    with open("output_text.txt", "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)
