import fitz
import string
import re
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

def is_scanned_pdf(pdf_path, start_page=4, end_page=None, max_words_threshold=50):
    try:
        with fitz.open(pdf_path) as doc:
            if end_page is None:
                end_page = doc.page_count

            for page_number in range(start_page, end_page):
                page = doc.load_page(page_number)
                text = page.get_text()

                # Count the number of words in the page
                num_words = len(text.split())

                # If the number of words is below the threshold, consider it as a scanned page
                if num_words <= max_words_threshold:
                    scannedFiles.append(pdf_path)
                    return True

            return False

    except Exception as e:
        print(f"Error checking if PDF is scanned: {e}")
        return False


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
        # print(file_path,"*************")
        text =  extract_single_text(file_path)
        file_name = file_path[:-3]
        arr = file_name.split('\\')
        file_name = arr[len(arr)-1]
        file_name += "txt"
        # print("666666666666",file_name)
        
        save_text_to_file(destination_folder,file_name,text)

        
# extract_samples(constants.SOURCE_FOLDER_PATH,constants.EXTRACTED_SAMPLEs_FOLDER)
print("hi there!")
extract_samples("D:/A-erasi/MET Batch1","src\Data Extraction\Dirty Samples2")

# print the files that has no text
# print(errorFiles)
# print("Scanned Files: ",scannedFiles)
# print ("Number of scanned files: ",len(scannedFiles))


