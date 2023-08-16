import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Specify the folder path containing text files
folder_path = "C:/Users/maria/OneDrive/Desktop/Final Samples/Final Samples"

# Get a list of all text files in the folder
text_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]

# Initialize an empty string to hold the combined text
combined_text = ""

# Loop through each text file and append its content to the combined text
for text_file in text_files:
    file_path = os.path.join(folder_path, text_file)
    with open(file_path, "r", encoding="latin-1") as file:
        text = file.read()
        combined_text += text + " "  # Add a space between texts

# Generate the word cloud for the combined text
wordcloud = WordCloud(width=800, height=800, background_color="white").generate(combined_text)

# Display the word cloud using matplotlib
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Combined Word Cloud from Multiple Files")
plt.tight_layout(pad=0)

plt.show()
