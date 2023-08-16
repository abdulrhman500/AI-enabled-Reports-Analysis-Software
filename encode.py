import tensorflow as tf
import tensorflow_hub as hub
import re
import os

model_path = "D:\\universal-sentence-encoder_4"
# Load the Universal Sentence Encoder model
use_model = hub.load(model_path)

# Preprocess function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and punctuation
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    
    # Tokenize text
    tokens = text.split()
    
    # Join tokens back to text
    preprocessed_text = " ".join(tokens)
    return preprocessed_text

# Folder path containing text files
folder_path = "C:\\Users\\DELL\\Desktop\\USE\\Final Samples"

# Initialize a list to store preprocessed text
tasks_preprocessed = []

# Iterate through each text file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="cp1252", errors="replace") as file:
            tasks_text = file.read()
            preprocessed_task = preprocess_text(tasks_text)
            tasks_preprocessed.append(preprocessed_task)
# Generate embeddings for preprocessed "Tasks" sections
tasks_embeddings = use_model(tasks_preprocessed)
print(tasks_embeddings)
