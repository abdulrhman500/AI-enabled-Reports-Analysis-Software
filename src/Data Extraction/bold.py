import fitz
import re
import constants

def is_bold(font_flags):
    return bool(font_flags & (1 << 4))

def extract_bold_text_with_regex(pdf_file_path, regex_pattern):
    count = 0 #number of strings that matches reges
    count_list = []#contains the numbers(its order) of the bold string that matches regex 
    bold_text_with_regex = []
    doc = fitz.open(pdf_file_path)
    
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        blocks = page.get_text("dict", flags=11)["blocks"]
        
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    if re.search(regex_pattern, span["text"],re.IGNORECASE):
                        count += 1
                        if is_bold(span["flags"]):
                            count_list.append(count)
                            bold_text_with_regex.append(span["text"])
    
    doc.close()
    return bold_text_with_regex, count_list, count


if __name__ == "__main__":
    pdf_file_path = constants.FILE_PATH
    regex_pattern = r"Internship" 
    bold_text_list_with_string , count_list , count = extract_bold_text_with_regex(pdf_file_path,regex_pattern )
    print(count)
    print(count_list)
    for bold_text in bold_text_list_with_string:
        print(f"Bold Text: {str(bold_text).strip()}")

        