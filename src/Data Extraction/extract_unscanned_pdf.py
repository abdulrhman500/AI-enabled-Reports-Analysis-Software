import re
import string
from PyPDF2 import PdfReader
import get_start_end

def extract_unscanned_text(file_path)-> string:
    reader = PdfReader(file_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text
count = 0
def get_text(file_path)->string:
    extracted_text = extract_unscanned_text(file_path)
    choosen_start, choosen_end=0,0
    tasks_text=''
    # try:
    choosen_start, choosen_end = get_start_end.choose_start_end(file_path)
    
    tasks_text = extracted_text[choosen_start:choosen_end]

    # except Exception as e:
        # print("\033[31m"+"Error : "+file_path+"\033[31m",e)
    
    return tasks_text

if __name__ == "__main__":
    pass
    print("\nTASKS:\n\n"+get_text("E:\\NLP\\Internship\\Dirty Reports\\Dirty Files\\correct template\\(A) MariamAdelAbbasAbdelfattah_43-2045 - Mariam Enany.pdf"))


