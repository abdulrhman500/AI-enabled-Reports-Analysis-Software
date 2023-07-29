import string
import re
import extract_unscanned_pdf
import os
def extract_unscanned_text(file_path)-> string :
   return extract_unscanned_pdf.get_text(file_path) 

def extract_scanned_text(file_path)-> string:
    pass
def is_sccanned(file_path)-> bool:
    pass


def extract_single_text(file_path)-> string:
    # if is_sccanned(file_path):
        # return extract_scanned_text(file_path)
    # else:
        return extract_unscanned_text(file_path)
       
def get_pdfs_paths_in_folder(folder_path):
    pdf_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def save_text_to_file(folder_name, file_name, text):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w',encoding='utf-8') as file:
        file.write(text)

def extract_samples(folder_path) -> None:
    files_paths = get_pdfs_paths_in_folder(folder_path)
    for file_path in files_paths:
        # print(file_path,"*************")
        text =  extract_single_text(file_path)
        file_name = file_path[:-3]
        file_name += "txt"
        # print(text)
        save_text_to_file(folder_path,file_name,text)
    
extract_samples("E:\\NLP\\Internship\\Dirty Reports\\Dirty Files\\correct template")

