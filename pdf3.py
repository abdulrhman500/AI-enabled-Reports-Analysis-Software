import fitz  # PyMuPDF library

def extract_bold_underlined_words(pdf_path):
    bold_underlined_words = []

    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Iterate through all pages
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        # Get all text elements on the page
        text_elements = page.get_text("dict", flags=11)

        # Extract bold and underlined words from text elements
        for element in text_elements:
            text = element["text"]
            font_flags = element["flags"]

            # Check if the text is bold (font_flags value of 2) or underlined (font_flags value of 8)
            if font_flags & 2 or font_flags & 8:
                bold_underlined_words.extend(text.split())

    # Close the PDF file
    doc.close()

    return bold_underlined_words

if __name__ == "__main__":
    # Replace 'your_pdf_file.pdf' with the path to your PDF file
    pdf_path = 'C:/Users/DELL/Desktop/AI Intern/Hoda Ahmed Mostafa Desouki 49-14142.pdf'
    extracted_words = extract_bold_underlined_words(pdf_path)
    print(extracted_words)
