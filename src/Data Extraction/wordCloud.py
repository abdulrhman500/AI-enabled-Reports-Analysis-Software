import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

def get_pdfs_paths_in_folder(folder_path):
    pdf_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files




def generate_word_cloud_from_files(file_paths):
    # Combine text from all files
    combined_text = ""
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            combined_text += text + " "  # Add a space between texts

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate(combined_text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()

file_paths=get_pdfs_paths_in_folder("C:/Users/legion/Desktop/AI internship/AI-enabled-Reports-Analysis-Software/Final Samples")
print(file_paths[:3])
generate_word_cloud_from_files(file_paths)