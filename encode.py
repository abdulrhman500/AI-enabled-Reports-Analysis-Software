import tensorflow as tf
import tensorflow_hub as hub
import re
import os
import csv
import pandas as pd

model_path = "D:\\universal-sentence-encoder_4"
use_model = hub.load(model_path)

# Preprocess function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    tokens = text.split()
    preprocessed_text = " ".join(tokens)
    return preprocessed_text

# Folder path containing text files
folder_path = "C:\\Users\\DELL\\Desktop\\USE\\AI-enabled-Reports-Analysis-Software\\Final Samples"

# Initialize lists to store preprocessed text, filenames, embeddings, and decisions
tasks_preprocessed = []
file_names = []
embeddings = []
decisions = []

# Specify the full path to the Excel file
excel_file = "C:\\Users\\DELL\\Desktop\\USE\\AI-enabled-Reports-Analysis-Software\\MET - Batch 1.xlsx"

# Read the Excel sheet
df = pd.read_excel(excel_file)

# Iterate through each text file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="cp1252", errors="replace") as file:
            tasks_text = file.read()
            preprocessed_task = preprocess_text(tasks_text)
            tasks_preprocessed.append(preprocessed_task)
            file_names.append(filename)

        # Find matching student in the DataFrame based on name
        matching_students = df[df['Student Name '].apply(lambda x: isinstance(x, str) and x in filename)]

        if not matching_students.empty:
            decision = matching_students['Academic Feedback'].values[0]
        else:
            # Extract numeric part of the filename
            file_number = re.search(r'\d+[-_]\d+', filename)
            if file_number:
                file_number = file_number.group()
                matching_students = df[df['GUC Student ID No.'].apply(lambda x: isinstance(x, str) and x == file_number)]
            else:
                matching_students = pd.DataFrame()

            if not matching_students.empty:
                decision = matching_students['Academic Feedback'].values[0]
            else:
                decision = "No matching student"

        decisions.append(decision)


# Generate embeddings for preprocessed "Tasks" sections
tasks_embeddings = use_model(tasks_preprocessed)

# Collect embeddings in a list
for embedding in tasks_embeddings:
    embeddings.append(embedding.numpy().tolist())

# Save data to a CSV file
csv_file = "tasks_embeddings_with_decisions.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["File Name", "Embedding", "Academic Feedback"])
    for file_name, embedding, decision in zip(file_names, embeddings, decisions):
        writer.writerow([file_name, embedding, decision])

print(f"Data saved to {csv_file}")
