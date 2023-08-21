import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

TfVectorizer = TfidfVectorizer()

def preprocess(text:str):
    text = re.sub('\n', '', text)
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
     #Print the lemmatized tokens to debug
    # for token in doc:
    #    print(token.lemma_, end=' ')
    # print()
    cleanedtext = [item.lemma_ for item in doc if not item.is_punct and not item.is_space and (not item.is_stop or item.is_alpha)]
    return " ".join(cleanedtext)

def apply_tfidf(corpus:list):
    return TfVectorizer.fit_transform(corpus)

folder_path = "C:/Users/legion/Desktop/AI internship/AI-enabled-Reports-Analysis-Software/Final Samples"
file_extension = '*.txt'

def main:
    corpus = []
    for file_path in glob.glob(os.path.join(folder_path, file_extension)):
        with open(file_path, encoding="latin-1") as file:
        text = file.read()
        corpus.append(preprocess(text))

    v.fit(corpus)
    transformed_output = v.fit_transform(corpus)
    # feature_names = v.get_feature_names_out()
    # dense = transformed_output.todense()
    # lst1 = dense.tolist()

    # df = pd.DataFrame(lst1, columns=feature_names)

    # tf_idf_counter = df.T.sum(axis=1)

    list_ = []
    for i in feature_names:
        list_.append(i)
    list_ = list(set(list_))
    print("unique features:", len(list_))
    print(list_)
    wordcloud = WordCloud(width=1200, height=800, background_color='white').generate(' '.join(list_))
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

if __name__ == '__main__':
    main()