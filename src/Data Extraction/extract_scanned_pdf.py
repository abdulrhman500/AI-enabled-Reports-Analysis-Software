import fitz
import re
import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def get_text(pdf_path):
    images = convert_from_path(pdf_path)
    # Specify the page number to start from
    start_page = 4  # Change this to the desired start page number

    # Extract text from images
    extracted_text = ""
    for page_num, image in enumerate(images, start=1):
        if page_num < start_page:
            continue  # Skip pages before the start page

        text = pytesseract.image_to_string(image, lang='eng')
        extracted_text += text + "\n"

    # Specify a regular expression pattern to match bold titles
    bold_title_pattern = r'^[A-Za-z\s]+:'  # Adjust this pattern as needed

    # Process the extracted text to identify titles and paragraphs
    lines = extracted_text.split('\n')
    sections = []
    current_section = {"title": "", "content": ""}
    for line in lines:
        if re.match(bold_title_pattern, line.strip()):  # Use the new pattern
            if current_section["title"]:
                current_section["title"] = re.sub(r'\(.*?\)', '', current_section["title"]).strip()  # Remove text in parentheses
                sections.append(current_section.copy())
                current_section = {"title": line.strip(), "content": ""}
            else:
                current_section["title"] = line.strip()
                current_section["content"] += line.strip() + " "  # Add the line directly after the title
        else:
            current_section["content"] += line.strip() + " "

    # Search for a section title that contains "Internship Performed Tasks:" within its title
    target_section_title = "Internship Performed Tasks:"
    target_section_content = ""
    max_content_length = 0

    for section in sections:
        # check if the target section title is found within the section title
        if target_section_title.lower() in section["title"].lower():
            # calculate content length (excluding the title)
            content_length = len(section["content"]) - len(target_section_title)
            
            # update if the current section has more content
            if content_length > max_content_length:
                max_content_length = content_length
                target_section_content = section["content"]
                target_section_title = section["title"]
            #check if the "Internship Performed Tasks:" title contains more than 3 words and if it does: 
            #add the extra words at the start of the content
            #and remove them from the title and remove "Internship Performed Tasks:" from the start of the content
            if len(target_section_title.split()) > 3:
                target_section_content = target_section_title + " " + target_section_content
                target_section_title = "Internship Performed Tasks:"
                target_section_content = target_section_content.replace("Internship Performed Tasks:", "")
            
            #check if the content contains "Internship Evaluation" and if it does:
            # remove it and everything after it from the content
            if "Internship Evaluation" in target_section_content:
                target_section_content = target_section_content.split("Internship Evaluation")[0]
            
            #check if if the content contains "Internship Performed Tasks:" and anything before it and if it does: 
            #remove it and everything before it from the content
            if "Internship Performed Tasks:" in target_section_content:
                target_section_content = target_section_content.split("Internship Performed Tasks:")[1]
    
    if not target_section_content:
        target_section_content = None

    return target_section_content

# Loop through all the pdf files in the folder 
# and extract the text from the pdf files
# and save the text in a text file

# import os
# path = "C:/Users/maria/OneDrive/Desktop/Internship Project/Dirty Reports/Dirty Files/OCR/working"
# for filename in os.listdir(path):
#     if filename.endswith(".pdf"):
#         pdf_path = os.path.join(path, filename)
#         text = get_text(pdf_path)
#         if text:
#             text_file = open(os.path.join(path, filename.replace(".pdf", ".txt")), "w")
#             text_file.write(text)
#             text_file.close()
#         else:
#             print("No text found in: " + filename)
#     else:
#         continue
