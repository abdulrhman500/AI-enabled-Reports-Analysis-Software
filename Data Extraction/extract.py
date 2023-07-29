from PyPDF2 import PdfReader
import re
start = -1
# 'Internship\s[a-z]*[\s]*Tasks[:]*[\s]*[\(\sNot\sless\sthan\s100\s[a-z]*\)]*[\s]*[\n](?!Internship)|Internship\sactivities'

def getStartPosition(extracted_text):
    start_position = -1
    tasks_pattern_1 = 'Internship[\s]*[a-z]*[\s]*Tasks'
    tasks_pattern_2 = 'Internship\s[^\n]*activities'
    tasks_match_1 = re.finditer(
        tasks_pattern_1, extracted_text, re.IGNORECASE | re.DOTALL)
    tasks_match_2 = re.finditer(
        tasks_pattern_2, extracted_text, re.IGNORECASE | re.DOTALL)
    matches = []
    if re.search(
        tasks_pattern_1, extracted_text, re.IGNORECASE | re.DOTALL) is not None and re.search(
        tasks_pattern_2, extracted_text, re.IGNORECASE | re.DOTALL) is None:
        print("start1")
        for match_obj in tasks_match_1:
            matches.append(match_obj)
        print(matches)
        if matches:
            start_position = matches[len(matches)-1].end()
    elif re.search(
        tasks_pattern_1, extracted_text, re.IGNORECASE | re.DOTALL) is None and re.search(
        tasks_pattern_2, extracted_text, re.IGNORECASE | re.DOTALL) is not None:
        print("start2")
        for match_obj in tasks_match_2:
            matches.append(match_obj)
        print(matches)
        if matches:
            start_position = matches[len(matches)-1].end()
    else:
        print("start3")
        match1 = []
        match2 = []
        for match_obj in tasks_match_1:
            match1.append(match_obj)
    
        for match_obj in tasks_match_2:
            match2.append(match_obj)
        print(match1)
        print(match2)
        if(match1[len(match1)-1].end()< match2[len(match2)-1].end() and len(match1)==1 and len(match2)==1):
            start_position = match2[len(match2)-1].end()
        else:
            start_position = match2[len(match2)-1].end()


    start = start_position
    print(start)
    return start_position


def getEndPosition(extracted_text):
    end_position = -1
    end_pattern_1= 'Internship[\s]*Evaluation'
    end_pattern_2 = 'Evaluation[\s]*of[\s]*[a-z]*[\s]*Internship'
    end_match_1 = re.finditer(end_pattern_1, extracted_text,
                            re.IGNORECASE | re.DOTALL)
    end_match_2 = re.finditer(end_pattern_2, extracted_text,
                        re.IGNORECASE | re.DOTALL)
    matches = []
    if re.search(end_pattern_1, extracted_text,
                            re.IGNORECASE | re.DOTALL) is not None and re.search(end_pattern_2, extracted_text,
                            re.IGNORECASE | re.DOTALL) is None:
        for match_obj in end_match_1:
            matches.append(match_obj)
        print(matches)
        if matches:
            end_position = matches[len(matches)-1].start()
        print("end1")
    elif re.search(end_pattern_1, extracted_text,
                            re.IGNORECASE | re.DOTALL) is None and re.search(end_pattern_2, extracted_text,
                            re.IGNORECASE | re.DOTALL) is not None:
        for match_obj in end_match_2:
            matches.append(match_obj)
        print(matches)
        if matches:
            end_position = matches[len(matches)-1].start()
        print("end2")
    elif re.search(end_pattern_1, extracted_text,
                            re.IGNORECASE | re.DOTALL) is None and re.search(end_pattern_2, extracted_text,
                            re.IGNORECASE | re.DOTALL) is None:
        end_pattern = 'Conclusion'
        end_match = re.search(end_pattern,extracted_text,re.IGNORECASE | re.DOTALL)
        print("Con", end_match)
        if end_match:
            end_position = end_match.start()
        print("end3")

    else:
        print("end4")
        match1 = []
        match2 = []
        print(match1)
        print(match2)
        for match_obj in end_match_1:
            match1.append(match_obj)
    
        for match_obj in end_match_1:
            match2.append(match_obj)

        if(match2[len(match2)-1].start()>start and match1[len(match1)-1].start()>start):
            end_position = min(match2[len(match2)-1].start()-start,match1[len(match1)-1].start()) 
        elif(match2[len(match2)-1].start()<start):
            end_position = match1[len(match1)-1].start()
        elif(match1[len(match1)-1].start()<start):
            end_position = match2[len(match2)-1].start()

    return end_position


def getTextFromFile(path):
    reader = PdfReader(path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()

    start_position = getStartPosition(extracted_text)
    end_position = getEndPosition(extracted_text)
    text_after_tasks = extracted_text[start_position:end_position]

    return text_after_tasks


pdf_file_path = '(A) Malik Sohile Ismail 43-12688 - Malik Ismail.pdf'
extracted_text = getTextFromFile(pdf_file_path)
print(extracted_text)
