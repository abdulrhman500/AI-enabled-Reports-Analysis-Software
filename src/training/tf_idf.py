import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


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


def preprocess_document(document:str):
    words = word_tokenize(document)
    filtered_words = [stemmer.stem(word) for word in words if word.lower() not in stop_words and not is_number(word) and not is_single_letter(word) and not is_line(word)]
    return " ".join(filtered_words)


def vectorize(preprocessed_corpus):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_corpus)
    tfidf_array = tfidf_matrix.toarray()
    return tfidf_array

def apply_tf_idf(text:list):
    return vectorize(text)
