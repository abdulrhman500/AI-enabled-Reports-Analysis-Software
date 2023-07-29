import PyPDF2

# def extract_text_from_headline(pdf_path, headline):
#     with open(pdf_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfReader(file)
        
#         full_text = ""
#         for page in pdf_reader.pages:
#             full_text += page.extract_text()

#         # Find the index of the headline in the full text (case-insensitive)
#         start_index = full_text.lower().find(headline.lower())
#         end_index = full_text.lower().find(headline2.lower())

#         if start_index != -1:
#             # Extract text from the headline until the end of the document
#             extracted_text = full_text[start_index:end_index]
#             return extracted_text
#         else:
#             return None

# # Example usage:
# pdf_path = 'C:/Users/DELL/Desktop/AI Intern/Hoda Ahmed Mostafa Desouki 49-14142.pdf'
# headline = 'Internship Performed Tasks'  # Replace with the desired headline
# headline2 = 'Internship working conditions'
# extracted_text = extract_text_from_headline(pdf_path, headline)
# if extracted_text:
#     print(extracted_text)
# else:
#     print("Headline not found in the PDF.")
# import fitz  # PyMuPDF library

# def is_bold_and_underlined(word):
#     # Check if the word is both bold and underlined
#     font_flags = word[5]
#     return font_flags & 2 and font_flags & 8

# def extract_bold_underlined_text(pdf_path, target_text):
#     bold_underlined_text = []

#     # Open the PDF file
#     doc = fitz.open(pdf_path)

#     # Flag to indicate if we've found the target text
#     found_target_text = False

#     # Iterate through all pages
#     for page_num in range(doc.page_count):
#         page = doc.load_page(page_num)

#         # Get all words on the page along with their formatting information
#         words = page.get_text("words", flags=fitz.TEXT_INHIBIT_SPACES | fitz.TEXT_PRESERVE_WHITESPACE)

#         # Extract bold and underlined text that matches the target text
#         for word in words:
#             if is_bold_and_underlined(word):
#                 if target_text in word[4]:  # Check the formatting for bold and underlined
#                     found_target_text = True
#                 if found_target_text:
#                     bold_underlined_text.append(word[4].strip())  # The text of the word is at index 4

#     # Close the PDF file
#     doc.close()

#     return bold_underlined_text

# if __name__ == "__main__":
#     # Replace 'your_pdf_file.pdf' with the path to your PDF file
#     pdf_path = 'C:/Users/DELL/Desktop/AI Intern/Hoda Ahmed Mostafa Desouki 49-14142.pdf'
#     target_text = 'tasks'  # Replace with the desired target text
#     extracted_text = extract_bold_underlined_text(pdf_path, target_text)
    
#     if extracted_text:
#         print("".join(extracted_text))
#     else:
#         print("No matching bold and underlined text found.")

# import fitz  # PyMuPDF library

# def is_bold_or_underlined(word):
#     # Check if the word is either bold or underlined
#     font_flags = word[5]
#     return font_flags & 2 or font_flags & 8

# def extract_bold_or_underlined_text(pdf_path, target_text):
#     bold_or_underlined_text = []

#     # Open the PDF file
#     doc = fitz.open(pdf_path)

#     # Flag to indicate if we've found the target text
#     found_target_text = False

#     # Iterate through all pages
#     for page_num in range(doc.page_count):
#         page = doc.load_page(page_num)

#         # Get all words on the page along with their formatting information
#         words = page.get_text("words", flags=fitz.TEXT_INHIBIT_SPACES | fitz.TEXT_PRESERVE_WHITESPACE)

#         # Extract bold or underlined text until the word "evaluation" is found
#         for word in words:
#             if is_bold_or_underlined(word):
#                 if target_text in word[4]:  # Check the formatting for bold or underlined
#                     found_target_text = True

#             # Append the text to the list only if we have found the target word and not found "evaluation"
#             if found_target_text and "evaluation" not in word[4]:
#                 bold_or_underlined_text.append(word[4].strip())

#     # Close the PDF file
#     doc.close()

#     # Combine the extracted text as paragraphs
#     extracted_paragraphs = " ".join(bold_or_underlined_text)

#     return extracted_paragraphs

# if __name__ == "__main__":
#     # Replace 'your_pdf_file.pdf' with the path to your PDF file
#     pdf_path = 'C:/Users/DELL/Desktop/AI Intern/Omar-Mohamed-Gamaleldin-Helmy-Abuomar_43-3960 - Omar Gamal.pdf'
#     target_text = 'tasks'  # Replace with the desired target text
#     extracted_text = extract_bold_or_underlined_text(pdf_path, target_text)
    
#     if extracted_text:
#         print(extracted_text)
#     else:
#         print("No matching bold or underlined text found.")




import fitz  # PyMuPDF library

def is_bold_or_underlined(word):
    # Check if the word is either bold or underlined
    font_flags = word[5]
    return font_flags & 2 or font_flags & 8

def extract_bold_or_underlined_text(pdf_path, target_text):
    bold_or_underlined_text = []

    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Flag to indicate if we've found the target text
    found_target_text = False

    # Iterate through all pages
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        # Get all words on the page along with their formatting information
        words = page.get_text("words", flags=fitz.TEXT_INHIBIT_SPACES | fitz.TEXT_PRESERVE_WHITESPACE)

        # Extract bold or underlined text until the word "Internship evaluation" is found
        for word in words:
            if is_bold_or_underlined(word):
                if target_text in word[4]:  # Check the formatting for bold or underlined
                    found_target_text = True

            # Append the text to the list only if we have found the target word and not found "Internship evaluation"
            if found_target_text:
                bold_or_underlined_text.append(word[4].strip())
                if "Internship" in word[4]:  # Stop extracting when "Internship evaluation" is found
                    found_target_text = False
                    break

    # Close the PDF file
    doc.close()

    # Combine the extracted text as paragraphs
    extracted_paragraphs = " ".join(bold_or_underlined_text)

    return extracted_paragraphs

if __name__ == "__main__":
    # Replace 'your_pdf_file.pdf' with the path to your PDF file
    pdf_path = 'C:/Users/DELL/Desktop/AI Intern/Salma_ElSayed_43_6801 - Salma ElSayed.pdf'
    target_text = 'tasks'  # Replace with the desired target text
    extracted_text = extract_bold_or_underlined_text(pdf_path, target_text)
    
    if extracted_text:
        print(extracted_text)
    else:
        print("No matching bold or underlined text found.")


