from PyPDF2 import PdfReader
import re
import constants
import bold


def find_positions(regex_pattern, text):
    positions = []
    i = 1
    for match in re.finditer(regex_pattern, text, re.IGNORECASE):
        # print(i,"   ", regex_pattern)
        i+=1
        positions.append(match.start()) 
        print(match)
    return positions


def getTextFromFile(path):
    reader = PdfReader(path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text


def check(terminal_list, file_path, regex):
    bolds, count_list, count = bold.extract_bold_text_with_regex(file_path, regex)
   
    ret = []
    if len(count_list) == 1:
        # if bolds[count_list[0]-1].lower()=="Internship Evaluation & Reporting".lower():
        #     return []
        ret =[terminal_list[count_list[0]-1]]
    
    else:
        print(terminal_list)
        print(count_list)
        if(len(count_list)<1):
            return []
        ret = [terminal_list[idx - 1] for idx in count_list]
        print("111**777777777777777777777777777777777777777777777777777777777777777777777777777777777777***",ret , bolds)
        # if len(ret)==1:
            # print("**777777777777777777777777777777777777777777777777777777777777777777777777777777777777***",ret , bolds)
            # if bolds[ret[0]-1].lower()=="Internship Evaluation & Reporting".lower():
                # return []
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
        if start > end :
            continue
        if text_length > max_length:
            max_length = text_length
            s = start
            e = end
    print(s,e,"REturned form apply algo")        
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

def add_spaces_to_regex(regex):
    modified_regex = re.sub(r'(?<=\S)(?=\S)', r'\s*', regex)
    return modified_regex

def choose_start_end(file_path):
    choosen_start = -1
    choosen_end = -1
    extracted_text = getTextFromFile(file_path)
    print(extracted_text,"1...........Extracted TEXT")
    regex_start = [
        r'\s*Internship activities and performed tasked\s*',
        r"\s*Internship\s*[a-zA-Z]*\s*Tasks\s*",  
        r"\s*Internship\s*Performed\s*(?:Tasks|activities)\s*",
        r"\s*Internship\s*performed\s*(?:Tasks|Activity)\s*",
         r'\s*Internship\s*[a-zA-Z]*\s*(?:activities?|activity?)\s*',
        r"performed\s*(?:task|activity)",
        r"performed\s*(?:tasks|activities)",
        r"task|activity|tasks|activities"
    ]
    regex_end = [
        r'\s*Internship\s*Evalua\s*tion\s*:?\s*',
        r'[\s]Evaluation[\s]of[\s]*[a-zA-z]*[\s]*Internship[\s]*:?[\s]*'
    ]

#     regex_start = [
#         # r'\s*I\s*n\s*t\s*e\s*r\s*n\s*s\s*h\s*i\s*p\s*\s*[a-zA-Z]*\s*T\s*a\s*s\s*k\s*s\s*',
#         r'\s*I\s*n\s*t\s*e\s*r\s*n\s*s\s*h\s*i\s*p\s*\s*P\s*e\s*r\s*f\s*o\s*r\s*m\s*e\s*d\s*\s*(?:T\s*a\s*s\s*k\s*s\s*|a\s*c\s*t\s*i\s*v\s*i\s*t\s*i\s*e\s*s\s*)\s*',
#         r'\s*I\s*n\s*t\s*e\s*r\s*n\s*s\s*h\s*i\s*p\s*\s*p\s*e\s*r\s*f\s*o\s*r\s*m\s*e\s*d\s*\s*(?:T\s*a\s*s\s*k\s*s\s*|A\s*c\s*t\s*i\s*v\s*i\s*t\s*y\s*)\s*',
#         r'p\s*e\s*r\s*f\s*o\s*r\s*m\s*e\s*d\s*\s*(?:t\s*a\s*s\s*k\s*|a\s*c\s*t\s*i\s*v\s*i\s*t\s*y\s*)',
#         r'p\s*e\s*r\s*f\s*o\s*r\s*m\s*e\s*d\s*\s*(?:t\s*a\s*s\s*k\s*s\s*|a\s*c\s*t\s*i\s*v\s*i\s*t\s*i\s*e\s*s\s*)',
#         r't\s*a\s*s\s*k\s*|a\s*c\s*t\s*i\s*v\s*i\s*t\s*y\s*'
# ]

#     regex_end = [
#         r'\s*I\s*n\s*t\s*e\s*r\s*n\s*s\s*h\s*i\s*p\s*\s*E\s*v\s*a\s*l\s*u\s*a\s*t\s*i\s*o\s*n\s*:\s*',
#         r'\s*I\s*n\s*t\s*e\s*r\s*n\s*s\s*h\s*i\s*p\s*\s*E\s*v\s*a\s*l\s*u\s*a\s*t\s*i\s*o\s*n\s*:?\s*',
#         r'\s*[\s]E\s*v\s*a\s*l\s*u\s*a\s*t\s*i\s*o\s*n\s*[\s]o\s*f\s*[\s]*[a-zA-Z]*[\s]*I\s*n\s*t\s*e\s*r\s*n\s*s\s*h\s*i\s*p\s*\s*:?\s*'
# ]


   
    for i in range(len(regex_start)):
        choosen_start = -1
        choosen_end = -1
        for j in range(len(regex_end)):
            print ("Start of inner loop " , j ," >>> regex start = ",regex_start[i], " regex end = ",regex_end[j])
            starts = find_positions(regex_start[i], extracted_text)
            ends = find_positions(regex_end[j], extracted_text)
           
            if len(ends) < 1:
                print("-----------------NO inital ends found---",regex_end[j])
                continue
            if len(starts) < 1:
                print("-----------------NO inital starts found---",regex_start[i])
                break

            print(starts,"------------- inital start indices--- ")
            print(ends,"------------- inital end indices--- ")
            
            temp_start = []
            temp_end = []
            # print("11111111111111,", starts)
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
                print(ends,"*1 ******************************",regex_end[j])
                temp_end = check(ends, file_path, regex_end[j])
                print(temp_end,"*2 ******************************")

            if len(temp_end) == 1:
                choosen_end = temp_end[0]
            
            ##############################
            
            if choosen_start == -1 and choosen_end == -1:
                print("APPLY ALGO *************-------**********----:")
                s,e= apply_algo(temp_start, temp_end,file_path)
                if(not is_valid_return(choosen_start,choosen_end)):
                    continue
                return s,e
            elif choosen_start == -1:
                print(" ****** end found and chooseing nearest start **** \n")
                choosen_start = get_nearest_start(temp_start, choosen_end)
            elif choosen_end ==-1:
                print(" ****** start found and chooseing nearest end **** \n")
                choosen_end = get_nearest_end(temp_end, choosen_start)
            
            if choosen_start != -1 and choosen_end != -1:
                if(not is_valid_return(choosen_start,choosen_end)):
                    print("Not Valid start and end", choosen_start, choosen_end)
                    continue
                return choosen_start, choosen_end    
            # print(choosen_end,"******************************")
    print("------the final return of  find start end ------***************** ",choosen_start, choosen_end)        
    return choosen_start, choosen_end
def is_valid_return(s,e):
    if(s>e):
        return False
    if(e-s<100):
        return False    
    return True    