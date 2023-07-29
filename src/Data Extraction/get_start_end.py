from PyPDF2 import PdfReader
import re
import constants
import bold


def find_positions(regex_pattern, text):
    positions = []
    i = 1
    for match in re.finditer(regex_pattern, text, re.IGNORECASE):
        print(i)
        i+=1
        positions.append(match.start()) 
    return positions


def getTextFromFile(path):
    reader = PdfReader(path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text


def check(terminal_list, file_path, regex):
    bolds, count_list, count = bold.extract_bold_text_with_regex(file_path, regex)
    print(bolds,"---------------")
    if len(count_list) == 1:
        return [terminal_list[count_list[0]-1]]
    else:
        print(terminal_list)
        print(count_list)
        if(len(count_list)<1):
            return []
        ret = [terminal_list[idx - 1] for idx in count_list]
        return ret


pdf_file_path = constants.FILE_PATH


def apply_algo(temp_start, temp_end,file_path):
    end_sorted = sorted(temp_end)
    start_sorted = sorted(temp_start)
    max_length = 0
    s = -1
    e = -1
    full_text= getTextFromFile(file_path)
    for start, end in zip(start_sorted, end_sorted):
        extracted_text = full_text[start:end]
        text_length = len(extracted_text)

        if text_length > max_length:
            max_length = text_length
            s = end
            e = start
    return s, e

def get_nearest_start(starts_list,end):
    starts_list = sorted(starts_list)
    for i in range(len(starts_list)-1,-1,-1):
        if(starts_list[i]<end):
            print(starts_list[i],"aaaaaaaaaaaaaaa")
            return starts_list[i]
    return -1

def get_nearest_end(ends_list,start):
    ends_list = sorted(ends_list)
    for i in range(len(ends_list)):
        if(ends_list[i]>start):
            print(ends_list[i],"qqqqqqqqqqq")
            return ends_list[i]
    return -1        
def choose_start_end(file_path):
    extracted_text = getTextFromFile(file_path)

    regex_start = [
        r"Internship[\s]*[a-z]*[\s]*Tasks"
        r"Internship[\s]*Performed[\s]*(?:Task|activities)",
        r"Internship\s*performed\s*(?:Tasks|Activity)",
        r"performed\s*(?:task|activity)",
        r"performed\s*(?:tasks|activities)",
        r"task|activity|tasks|activities"
    ]
    regex_end = [
        r'Internship[\s]*Evaluation',
        r'Evaluation[\s]of[\s]*[a-z]*[\s]*Internship'
    ]

    choosen_start = -1
    choosen_end = -1
    for i in range(len(regex_start)):
        for j in range(len(regex_end)):

            starts = find_positions(regex_start[i], extracted_text)
            ends = find_positions(regex_end[j], extracted_text)
            if len(ends) < 1:
                continue
            if len(starts) < 1:
                break

            temp_start = []
            temp_end = []
            print("11111111111111,", starts)
            if len(starts) == 1:
              
                choosen_start = starts[0]
            else:
                temp_start = check(starts, file_path, regex_start[i])


            if len(temp_start) == 1:
            
                choosen_start = temp_start[0]

            ###############################

            if len(ends) == 1:
                # print("222222222222,", ends)
              
                choosen_end = ends[0]
            else:
                # print(regex_start[i],"++++++++++")
                print(ends,"*1 ******************************")
                temp_end = check(ends, file_path, regex_end[j])
                print(temp_end,"*2 ******************************")

            if len(temp_end) == 1:
                choosen_end = temp_end[0]
            
            ##############################
            
            if choosen_start == -1 and choosen_end == -1:
                return apply_algo(temp_start, temp_end,file_path)
            elif choosen_start != -1 and choosen_end != -1:
                return choosen_start, choosen_end
            elif choosen_start == -1:
                choosen_start = get_nearest_start(temp_start, choosen_end)
            else:
                choosen_end = get_nearest_end(temp_end, choosen_start)
            # print(choosen_end,"******************************")
            return choosen_start, choosen_end
