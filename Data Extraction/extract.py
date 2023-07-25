import string
import re

def extract_unscanned_text(file_path)-> string :
   pass 
   #TODO call from extract_unscanned

def extract_scanned_text(file_path)-> string:
    pass
    #TODO use OCR 
def is_sccanned(file_path)-> bool:
    pass
    #TODO 

def extract_single_text(file_path)-> string:
    #function checks if the file is normal or scanned pdf  
    #then calls the appropriate function
    if is_sccanned(file_path):
        return extract_scanned_text(file_path)
    else:
        return extract_unscanned_text(file_path)
       

def extract_samples(folder_path) -> None:
    pass
    #TODO function loops over the folders then the retuned Text 
    #should be saved in folder called "Dirty Samples"
    #sample name can be something like "dirty_sample_15.txt"

