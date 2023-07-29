import PyPDF2

def extract_paragraph_from_page(pdf_path, page_number, paragraph_number):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        if page_number < 0 or page_number >= len(pdf_reader.pages):
            raise ValueError("Invalid page number. Page number should be in the range [0, {}]".format(len(pdf_reader.pages) - 1))
        
        page = pdf_reader.pages[page_number]
        text = page.extract_text()

        # Split the text into paragraphs based on line breaks or other patterns
        paragraphs = text.split('task')  # Adjust the splitting pattern based on the PDF's structure

        if paragraph_number < 0 or paragraph_number >= len(paragraphs):
            raise ValueError("Invalid paragraph number. Paragraph number should be in the range [0, {}]".format(len(paragraphs) - 1))
        paragraph = paragraphs[paragraph_number]
        start_index = paragraph.lower().find("task")
        extracted_text = paragraph[start_index:] if start_index != -1 else paragraph

        return paragraphs[paragraph_number]

# Example usage:
pdf_path = 'C:/Users/DELL/Desktop/AI Intern/Omar-Mohamed-Gamaleldin-Helmy-Abuomar_43-3960 - Omar Gamal.pdf'
page_number = 4  # Replace with the desired page number (0-indexed)
paragraph_number = 2  # Replace with the desired paragraph number (0-indexed)

try:
    extracted_paragraph = extract_paragraph_from_page(pdf_path, page_number, paragraph_number)
    print(extracted_paragraph)
except ValueError as e:
    print(e)