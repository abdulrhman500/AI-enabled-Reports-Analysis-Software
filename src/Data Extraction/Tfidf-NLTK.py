import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud

stemmer = PorterStemmer()
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


def is_line(text):
    patterns = [r"-+", r"=+", r"#+", r"\*+", r"_+"]  
    for pattern in patterns:
        if re.match(pattern, text):
            return True
    return False

def add_stop_words(words_list):
    global stop_words
    stop_words = stop_words.union(set(words_list))
    
def is_number(s):
    pattern = r'^[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$'
    return re.match(pattern, s) is not None
def is_single_letter(s):
    return len(s) == 1
def read_text(folder_path):
    list_ = []
    for root, _, files in os.walk(folder_path):
        for path in files:
            if path.lower().endswith('.txt'):
                temp = os.path.join(root, path)
                with open(temp, 'r', encoding='iso-8859-1') as file:
                    list_.append(file.read())
    return list_


def preprocess_document(document):
    words = word_tokenize(document)
    # print("Found words ",words)
    filtered_words = [stemmer.stem(word) for word in words if word.lower() not in stop_words and not is_number(word) and not is_single_letter(word) and not is_line(word)]
  #  print("Filtered words ",filtered_words)
    # print(" ".join(filtered_words))
    return " ".join(filtered_words)

def vectorize(preprocessed_corpus):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_corpus)
    tfidf_array = tfidf_matrix.toarray()
    features = vectorizer.get_feature_names_out()
    return features, tfidf_array

print("Hello vectorize")

if __name__ == "__main__":
    footer = "Student Career & Alumni Office scad@guc.edu.eg | German in Cairo New Cairo City - Main Entrance Al Tagamoa Al Khames Egypt "
    punctuation_marks = ['!', '"', '#', '$', '%', '&', "'",'`', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
    additional_stop_words=["'s","’","``","''","●",'us','edu','eg','scad','owner','ba']
    footer_words = footer.lower().split()
    # print(footer_words)
    # return 0
    add_stop_words(footer_words)
    add_stop_words(punctuation_marks)
    add_stop_words(additional_stop_words)
    # print(stop_words)
    # return 0
    # print("------------************",stop_words)
    corpus = read_text('D:/AI-enabled-Reports-Analysis-Software internship/Final Samples')
    preprocessed_corpus = [preprocess_document(doc) for doc in corpus]
    print("Number of features:", len(preprocessed_corpus))
    # text = "The quick brown german fox jumps over the lazy dog, but the dog is not amused."
    # preprocessed_corpus = [preprocess_document(text)]
    features_list = []
    for filtered_words in preprocessed_corpus:
        try:
            features, tfidf_array = vectorize([filtered_words])
            features_list.append(features)
        except Exception as e:
            print("Error:", e)
            continue
            
    print("Number of documents processed:", len(features_list))
    total_features = sum(len(features) for features in features_list)
    print("Total features:", total_features)
    # print("features:", features_list)
    list_=[]
    for i in features_list:
        for j in i:
            list_.append(j)
    list_=list(set(list_))        
    print("unique features:", len(list_))
    print(list_)
    wordcloud = WordCloud(width=1200, height=800, background_color='white').generate(' '.join(list_))
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    #plt.show()
    plt.show(block=True)
    #plt.savefig('wordcloud.png')