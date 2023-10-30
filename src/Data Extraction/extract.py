import string
import extract_unscanned_pdf
import extract_scanned_pdf
import constants
import os

# make an array of the files that has no text
errorFiles = []
scannedFiles = []

def extract_text(file_path)-> string :
   x = extract_unscanned_pdf.get_text(file_path)
   if x == "" or x == None:
       print("extracting scanned pdf")
       return extract_scanned_pdf.get_text(file_path)
   else:
       print("extracting unscanned pdf")
       return x

def extract_scanned_text(file_path)-> string:
    extract_scanned_pdf.get_text(file_path)

def extract_single_text(file_path)-> string:
    return extract_text(file_path)
       
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
    delete = False
    with open(file_path, 'w',encoding='utf-8') as file:
        if text is None:
            delete = True
        else:   
            file.write(text)
    if(delete):
        os.remove(file_path)

def extract_samples(source_folder_path,destination_folder) -> None:
    files_paths = get_pdfs_paths_in_folder(source_folder_path)
    for file_path in files_paths:
        text =  extract_single_text(file_path)
        file_name = file_path[:-3]
        arr = file_name.split('\\')
        file_name = arr[len(arr)-1]
        file_name += "txt"
        
        save_text_to_file(destination_folder,file_name,text)
       
extract_samples(constants.SOURCE_FOLDER_PATH,constants.EXTRACTED_SAMPLEs_FOLDER)