import fitz
import re
import PyPDF2


def is_bold(font_flags):
    return bool(font_flags & (1 << 4))


def find_positions(regex_pattern, text):
    positions = []
    for match in re.finditer(regex_pattern, text, re.IGNORECASE):
        print("MATCH####", match.group())
        positions.append(match.start())
    return positions


def check(terminal_list, file_path, regex):
    bolds, count_list, count = extract_bold_text_with_regex(file_path, regex)
    print(bolds, "---------------")
    if len(count_list) == 1:
        print("Terminal list", terminal_list)
        print("count list", count_list)
        print("RET", [terminal_list[count_list[0]-1]])
        if(count_list[0]-1<len(terminal_list) and count_list[0]-1>=0 ):
            return [terminal_list[count_list[0]-1]]
    else:
        print("Terminal list", terminal_list)
        print("count list", count_list)
        if (len(count_list) < 1):
            return []
        ret = []
        for idx in count_list:
            if(idx - 1 < len(terminal_list)):
                ret.append(terminal_list[idx-1])
        # ret = [terminal_list[idx - 1] for idx in count_list]
        print("RET2", ret)
        return ret


def extract_bold_text_with_regex(pdf_file_path, regex_pattern):
    count = 0
    count_list = []
    bold_text_with_regex = []
    doc = fitz.open(pdf_file_path)

    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE, sort ='true')["blocks"]
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    # font_name = fitz.Font(span["font"]).name
                    # print("FONT   ",font_name)
                    if re.findall(regex_pattern, span["text"], re.IGNORECASE):
                        match = re.findall(regex_pattern, span["text"], re.IGNORECASE)
                        # print("MATCH LEN",len(match))
                        count += len(match)
                        print("Count",count)
                        print(span["text"])
                        print("FLAGS*** ",span["flags"])
                        # print(is_bold(span["flags"]))
                        if is_bold(span["flags"]):
                            count_list.append(count)
                            print("count list", count_list)
                            bold_text_with_regex.append(span["text"])


    doc.close()
    return bold_text_with_regex, count_list, count


def extract_text_from_PDF(pdf_path):
    # with open(pdf_path, 'rb') as file:
    #     pdf_reader = PyPDF2.PdfReader(file)
    #     full_text = ""
    #     for page in pdf_reader.pages:
    #         full_text += page.extract_text()
    doc = fitz.open(pdf_path)
    full_text  = ""
    for page in doc:
        full_text += page.get_text(sort ="true")
    return full_text


def extract_text_from_headline(pdf_path, start, end):
    # with open(pdf_path, 'rb') as file:
    #     pdf_reader = PyPDF2.PdfReader(file)
    #     full_text = ""
    #     for page in pdf_reader.pages:
    #         full_text += page.extract_text()
    doc = fitz.open(pdf_path)
    full_text  = ""
    for page in doc:
        full_text += page.get_text(sort ="true")
        # if len(start)!=0:
            # extracted_text = full_text[start[len(start)-1]:end[len(end)-1]
    extracted_text = full_text[start:end]
    return extracted_text
    # else:
    #     return None


if __name__ == "__main__":
    pdf_file_path = ""
    regex_pattern_start1 = "task"
    regex_pattern_start2 = "activities"
    regex_pattern_end = "evaluation"

    text = extract_text_from_PDF(pdf_file_path)
    print("--------------------------------")
    print(text)
    print("--------------------------------")
    pos_start1 = find_positions(regex_pattern_start1, text)
    pos_start2 = find_positions(regex_pattern_start2, text)
    pos_end = find_positions(regex_pattern_end, text)
    print("pos_start1", pos_start1)
    print("pos_start2", pos_start2)
    print("pos_end ", pos_end)
    start1 = check(pos_start1, pdf_file_path, regex_pattern_start1)
    start2 = check(pos_start2, pdf_file_path, regex_pattern_start2)
    end = check(pos_end, pdf_file_path, regex_pattern_end)
    print("start1", start1)
    print("start2 ", start2)
    print("end ", end)

    not_bold_regex_start1 = "Internship[\s]*[a-z | A-Z]*task"
    not_bold_pos_start1 = find_positions(not_bold_regex_start1, text)
    if (len(start2) > 0):
        s = start2[len(start2)-1]
    elif (len(start1) > 0):
        s = start1[len(start1)-1]
    elif(len(pos_start2)> 0):
        s = pos_start2[len(pos_start2)-1]
    elif(len(not_bold_pos_start1) >0):
        s = not_bold_pos_start1[len(not_bold_pos_start1)-1]
    else:
        s = -1
    if (len(end) > 0):
        e = end[len(end)-1]
    elif(len(pos_end) > 0):
        e = pos_end[len(pos_end)-1]
    else:
        e = -1
    print(s)
    print(e)
    print("1111111111")
    extracted_text = extract_text_from_headline(pdf_file_path, s, e)
    extracted_text = re.sub('\n', '', extracted_text)
    if len(extracted_text) >48:
        print(extracted_text)
    else:
        if(len(pos_start2)> 0):
            s = pos_start2[len(pos_start2)-1]
        elif(len(not_bold_pos_start1) >0):
            s = not_bold_pos_start1[len(not_bold_pos_start1)-1]
        else:
            s =-1
        if(len(pos_end) > 0):
           print("POS_END", pos_end)
           e = pos_end[len(pos_end)-1]
        else:
           e = -1
        print(s)
        print(e)
        print("22222222222")

        extracted_text = extract_text_from_headline(pdf_file_path, s, e)
        if(extracted_text):
            print(extracted_text)
        else:
            i = 1
            while(s>e):
                print("YARAB   ",len(pos_start2)-i )
                if(len(pos_start2)-i >= 0):
                    s = pos_start2[len(pos_start2)-i]
                    i+=1
                else:
                    print("Break1")
                    break
                print(s)
                print(e)
            i = 1
            while(s>e):
                print("Yarab  ", len(not_bold_pos_start1)-i )
                if(len(not_bold_pos_start1)-i >= 0):
                    s = not_bold_pos_start1[len(not_bold_pos_start1)-i]
                    i+=1
                else:
                    print("HEadline not found")
                    break
                print(s)
                print(e)
            extracted_text = extract_text_from_headline(pdf_file_path, s, e)
            if(extracted_text):
                print(extracted_text)
            else:
                print("3333333333")