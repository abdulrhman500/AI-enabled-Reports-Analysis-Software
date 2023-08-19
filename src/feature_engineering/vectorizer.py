import os
import tensorflow as tf
import tensorflow_hub as hub
from Data import Data #import the Data class from the Data.py file
import time
import pandas as pd 
from USE import apply_USE #import the apply_USE function from USE.py file
from spacyTF-IDF import preprocess, apply_tfidf

def get_decision(file_path)-> int:
    return 1  #TODO 

def load_decision(execl_sheet_path) -> list:
    #TODO: load the decisions from the excel sheet
    excel_data = pd.read_excel(execl_sheet_path)  
    decisions = [] 
    
    for index, row in excel_data.iterrows():
        guc_student_id = row['GUC Student ID No.']
        student_name = row['Student Name']
        academic_feedback = row['Academic Feedback']
        company_name = row['Company Name']
        
        # decision logic here
        decision = ""  
        decisions.append(decision)
    
    return decisions

def read_text(file_path) -> str:
    text = None
    with open(file_path, 'r', encoding='iso-8859-1') as f:
        text = f.read()
    return text    

def get_file_paths(folder_path) -> list:
    file_paths=[]
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        file_paths.append(file_path)
    return file_paths

def vectorize_documents_one_by_one(start_idx, end_idx, data_obj, vectorization_technique) -> Data:
    for idx in range(start_idx, end_idx):
        file_path = file_paths[idx]
        text = read_text(file_path)
        file_name = file_path.split('\\')[-1]
        vector = vectorization_technique(text)
        decision = get_decision(file_path)
        data_obj.add_data(file_name, vector, decision)
    return data_obj

def vectorize_documents_once(start_idx, end_idx, data_obj, vectorization_technique,preprocessing=None) -> Data:
#used for Tf-idf
    
    texts= []
    file_names = []
    vectors = []
    decisions = [] 
   
    for idx in range(start_idx, end_idx):
        file_path = file_paths[idx]
        text = read_text(file_path)
        if (preprocessing != None):
            text = preprocessing(text)
        texts.append(tet)
        file_names.append(file_path.split('\\')[-1])
        decisions.append(get_decision(file_path))
    vectors = vectorization_technique(texts)     
    
    for idx in range(len(texts)):
        text = texts[idx]
        file_name = file_names[idx]
        vector=vectors[idx]
        decision = decisions[idx]
        data_obj.add_data(file_name, vector, decision)
    
    return data_obj


folder_path = "E:\\NLP\\Final Samples" #path to the folder containing the Text files
execl_sheet_path = "" #path to the excel sheet containing the decisions
decisions = None
file_paths = get_file_paths(folder_path)


def main():
    start_time = time.time()
    # load_decision(execl_sheet_path)
    data_obj = Data(len(file_paths)) 
    vectorize_documents_once(0, len(file_paths), data_obj, apply_tfidf, preprocess)
    # vectorize_documents_one_by_one(0, len(file_paths), data_obj, apply_USE)
    
    data_obj.save_to_csv("a.csv")
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} s")
    print(f"Total number of files: {len(file_paths)}")

if __name__ == "__main__":
    main()
    
