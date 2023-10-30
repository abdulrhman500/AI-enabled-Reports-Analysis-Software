import re
import string
import fitz
import constants

def is_bold(font_flags):
    return bool(font_flags & (1 << 4))


def find_positions(regex_pattern, text):
    positions = []
    for match in re.finditer(regex_pattern, text, re.IGNORECASE):
        positions.append(match.start())
    return positions


def check(terminal_list, file_path, regex):
    bolds, count_list, count = extract_bold_text_with_regex(file_path, regex)
    ret=[]
    if len(count_list) == 1:
        if(count_list[0]-1<len(terminal_list) and count_list[0]-1>=0 ):
            ret= [terminal_list[count_list[0]-1]]
    else:
        if (len(count_list) < 1):
            return []
        ret = []
        for idx in count_list:
            if(idx - 1 < len(terminal_list)):
                ret.append(terminal_list[idx-1])
    return ret


def extract_bold_text_with_regex(pdf_file_path, regex_pattern):
    count = 0
    count_list = []
    bold_text_with_regex = []
    doc = fitz.open(pdf_file_path)

    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE , sort='true')["blocks"]
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    if re.findall(regex_pattern, span["text"], re.IGNORECASE):
                        match = re.findall(regex_pattern, span["text"], re.IGNORECASE)
                        count += len(match)
                        if is_bold(span["flags"]):
                            count_list.append(count)
                            bold_text_with_regex.append(span["text"])


    doc.close()
    return bold_text_with_regex, count_list, count

def extract_text_from_PDF(pdf_path):
    doc = fitz.open(pdf_path)
    full_text  = ""
    for page in doc:
        full_text += page.get_text(flags=fitz.TEXT_PRESERVE_WHITESPACE ,sort ="true")
    return full_text

def get_start_end(pdf_file_path):
    regex_pattern_start1 = constants.REGEX_PATTERN_START1
    regex_pattern_start2 = constants.REGEX_PATTERN_START2
    regex_pattern_end = constants.REGEX_PATTERN_END

    text = extract_text_from_PDF(pdf_file_path)
    pos_start1 = find_positions(regex_pattern_start1, text)
    pos_start2 = find_positions(regex_pattern_start2, text)
    pos_end = find_positions(regex_pattern_end, text)

    start1 = check(pos_start1, pdf_file_path, regex_pattern_start1)
    start2 = check(pos_start2, pdf_file_path, regex_pattern_start2)
    end = check(pos_end, pdf_file_path, regex_pattern_end)

    not_bold_regex_start1 = "Internship[\s]*[a-z | A-Z]*task"
    not_bold_pos_start1 = find_positions(not_bold_regex_start1, text)

    if (len(start2) > 0):
        s = start2[len(start2)-1]
    elif (len(start1) > 0):
        s = start1[len(start1)-1]
    else:
        s = -1
    if (len(end) > 0):
        e = end[len(end)-1]
    else:
        e = -1
    return s,e, pos_start2, pos_end, not_bold_pos_start1, pos_end

def extract_text_from_headline(pdf_path, start, end):
    doc = fitz.open(pdf_path)
    full_text  = ""
    for page in doc:
        full_text += page.get_text(flags=fitz.TEXT_PRESERVE_WHITESPACE , sort ="true")
    extracted_text = full_text[start:end]
    return extracted_text

def get_text(file_path)->string:
    start, end=0,0
    extracted_text=''
    try:
        start, end, pos_start2, pos_end, not_bold_pos_start1, pos_end = get_start_end(file_path)
        extracted_text = extract_text_from_headline(file_path,start,end)
        extracted_text = re.sub('\n', '', extracted_text)
        if len(extracted_text) > 48:
            print(extracted_text)
        else:
            extracted_text=''
    except Exception as e:
        print("[ERROR] ",e) 
    return extracted_text