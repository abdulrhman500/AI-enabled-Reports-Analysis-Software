import tensorflow as tf
import tensorflow_hub as hub
import re
import pandas as pd

# specify the file path to the universal sentence encode model
model_path = ""
use_model = hub.load(model_path)

# Preprocess function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    tokens = text.split()
    preprocessed_text = " ".join(tokens)
    return preprocessed_text

# Specify the path to the CSV file
csv_file_path = ""

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Initialize a list to store embeddings
embeddings = []

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    text = row['text']
    
    preprocessed_text = preprocess_text(text)
    
    # Generate embedding for preprocessed text
    text_embedding = use_model([preprocessed_text])
    embeddings.append(text_embedding[0].numpy().tolist())

# Add embeddings to the DataFrame
df['Embedding'] = embeddings

# Save the updated DataFrame back to the same CSV file
df.to_csv(csv_file_path, index=False)

print(f"Embeddings added to the existing CSV file.")
