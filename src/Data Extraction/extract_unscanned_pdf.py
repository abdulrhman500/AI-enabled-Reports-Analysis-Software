import re
import string
import fitz
import PyPDF2
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
from sklearn.feature_extraction import text
import constants



def is_bold(font_flags):
    return bool(font_flags & (1 << 4))


def find_positions(regex_pattern, text):
    positions = []
    for match in re.finditer(regex_pattern, text, re.IGNORECASE):
        #print("MATCH####", match.group())
        positions.append(match.start())
    return positions


def check(terminal_list, file_path, regex):
    bolds, count_list, count = extract_bold_text_with_regex(file_path, regex)
    #print(bolds, "---------------")
    ret=[]
    if len(count_list) == 1:
        # print("Terminal list", terminal_list)
        # print("count list", count_list)
        # print("RET", [terminal_list[count_list[0]-1]])
        if(count_list[0]-1<len(terminal_list) and count_list[0]-1>=0 ):
            ret= [terminal_list[count_list[0]-1]]
    else:
        # print("Terminal list", terminal_list)
        # print("count list", count_list)
        if (len(count_list) < 1):
            return []
        ret = []
        for idx in count_list:
            if(idx - 1 < len(terminal_list)):
                ret.append(terminal_list[idx-1])
        # ret = [terminal_list[idx - 1] for idx in count_list]
        # print("RET2", ret)
    return ret


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
                    if re.findall(regex_pattern, span["text"], re.IGNORECASE):
                        match = re.findall(regex_pattern, span["text"], re.IGNORECASE)
                        # print("MATCH LEN",len(match))
                        count += len(match)
                        # print("Count",count)
                        # print(span["text"])
                        if is_bold(span["flags"]):
                            count_list.append(count)
                            # print("count list", count_list)
                            bold_text_with_regex.append(span["text"])


    doc.close()
    return bold_text_with_regex, count_list, count


def extract_text_from_PDF(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()
    return full_text



def get_start_end(pdf_file_path):
    regex_pattern_start1 = constants.REGEX_PATTERN_START1
    regex_pattern_start2 = constants.REGEX_PATTERN_START2
    regex_pattern_end = constants.REGEX_PATTERN_END

    text = extract_text_from_PDF(pdf_file_path)
    pos_start1 = find_positions(regex_pattern_start1, text)
    pos_start2 = find_positions(regex_pattern_start2, text)
    pos_end = find_positions(regex_pattern_end, text)
    # print("pos_start1", pos_start1)
    # print("pos_start2", pos_start2)
    # print("pos_end ", pos_end)
    start1 = check(pos_start1, pdf_file_path, regex_pattern_start1)
    start2 = check(pos_start2, pdf_file_path, regex_pattern_start2)
    end = check(pos_end, pdf_file_path, regex_pattern_end)
    # print("start1", start1)
    # print("start2 ", start2)
    # print("end ", end)

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
    # print(s)
    # print(e)
    return s,e


def extract_text_from_headline(pdf_path, start, end):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text()
    extracted_text = full_text[start:end]
    return extracted_text

def get_text(file_path)->string:
    start, end=0,0
    tasks_text=''
    try:
        start, end = get_start_end(file_path)
        tasks_text = extract_text_from_headline(file_path,start,end)
    except Exception as e:
        print("[ERROR] ",e)

# def get_text(file_path) -> List[str]:
#     start, end = 0, 0
#     tasks_texts = []  # List to store multiple text documents
#     try:
#         start, end = get_start_end(file_path)
#         tasks_text = extract_text_from_headline(file_path, start, end)
#     except Exception as e:
#         print("[ERROR] ", e)
#     return tasks_texts

    
    return tasks_text

custom_stop_words = list(text.ENGLISH_STOP_WORDS) + ["", " "]  # Add custom stop words

# Words you want to exclude from the stop words list
words_to_exclude = ["al"]

# Filter out numeric values and combined stop words
filtered_stop_words = [word for word in custom_stop_words if not (word.strip().replace('.', '', 1).isdigit() or word.strip().isdigit())]
filtered_stop_words = [word for word in filtered_stop_words if word not in words_to_exclude]

def tf_idf(tasks):
    
    #vectorizer = TfidfVectorizer()
    #custom_stop_words = text.ENGLISH_STOP_WORDS.union([" ", "  "])  # Add custom stop words
    vectorizer = TfidfVectorizer(stop_words=filtered_stop_words)
    X = vectorizer.fit_transform(tasks).toarray()
    feature_names = vectorizer.get_feature_names_out()
    # preprocessed_text = ' '.join([word for word in extracted_text.split() if word not in custom_stop_words])
    # print("Preprocessed text: \n ", preprocessed_text)
    print(X.shape)
    print(X)
    print("feature_names: + \n")
    print(feature_names)
    return X,feature_names

#   *******MAINNNNNN*********
if __name__ == "__main__":
    pdf_file_path = "C:/Users/maria/OneDrive/Desktop/Internship Project/Dirty Reports/Dirty Files/correct template/(A) Ahmed Abdelazeem Omar 40-13742.pdf"
    #print("\nTASKS:\n\n"+get_text(pdf_file_path))
    extracted_text = get_text(pdf_file_path)
    print("Extracted text: \n ", extracted_text)
    tf_idf_result, feature_names = tf_idf([extracted_text])

    df = pd.DataFrame(tf_idf_result, columns=feature_names)
    
    # Display the DataFrame
    print(df)
    
    # Visualize the DataFrame using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')  # Turn off axis
    
    # Display the DataFrame as a table
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    
    # Adjust table layout
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Adjust table size
    
    plt.show()



# if __name__ == "__main__":
    pdf_directory = "D:/AI-enabled-Reports-Analysis-Software internship/Dirty Files/correct template/"
    pdf_files = os.listdir(pdf_directory)
    
    data = []
    document_names = []
    
    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(pdf_directory, pdf_file)
        document_names.append(pdf_file)
        
        # Extract text and preprocess
        start, end = get_start_end(pdf_file_path)
        tasks_text = extract_text_from_headline(pdf_file_path, start, end)
        preprocessed_text = ' '.join([word for word in tasks_text.split() if word not in custom_stop_words])
        
        data.append(preprocessed_text)
    
    # Apply TF-IDF on all documents
    tf_idf_result, feature_names = tf_idf(data)
    # Create a DataFrame for visualization
    df = pd.DataFrame(tf_idf_result, columns=feature_names, index=document_names)
    
    # Display the DataFrame as a table
    print(df)
    
    # Visualize the DataFrame using matplotlib
    plt.figure(figsize=(10, 6))
    plt.axis('off')  # Turn off axis labels
    plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    plt.show()