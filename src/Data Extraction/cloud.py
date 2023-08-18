import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Specify the folder path containing text files
folder_path = "C:/Users/legion/Desktop/AI internship/AI-enabled-Reports-Analysis-Software/Final Samples"

# Get a list of all text files in the folder
text_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]

# Loop through each text file
for text_file in text_files:
    # Construct the full path to the current text file
    file_path = os.path.join(folder_path, text_file)

    # Load the text data from the current file
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate(text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(f"Word Cloud for {text_file}")  # Add a title for the word cloud
    plt.tight_layout(pad=0)

    plt.show()
