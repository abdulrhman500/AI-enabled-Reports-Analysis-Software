import fitz
import re
import PyPDF2


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


if __name__ == "__main__":
    pdf_file_path = "C:/Users/DELL/Desktop/AI Intern/Rawan Ashraf 43-2692 - Rawan Ashraf(1).pdf"
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

pdf_path = "C:/Users/DELL/Desktop/AI Intern/Rawan Ashraf 43-2692 - Rawan Ashraf(1).pdf"

extracted_text = extract_text_from_headline(pdf_path, boldd)
if extracted_text:
    print(extracted_text)
else:
    print("Headline not found in the PDF.")