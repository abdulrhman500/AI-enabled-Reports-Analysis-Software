import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import glob
import pandas as pd
def preprocess(text):
    text = re.sub('\n', '', text)
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    cleanedtext = [item.lemma_ for item in doc if not item.is_stop and not item.is_punct and not item.is_space]     
    return " ".join(cleanedtext)

folder_path = '' #add your folder path here
file_extension = '*.txt'

corpus = []
for file_path in glob.glob(os.path.join(folder_path, file_extension)):
    with open(file_path, encoding="utf8") as file:
        text = file.read()
        corpus.append(preprocess(text))

v = TfidfVectorizer()
v.fit(corpus)
transformed_output = v.fit_transform(corpus)
feature_names = v.get_feature_names_out()
dense = transformed_output.todense()
lst1 = dense.tolist()

df = pd.DataFrame(lst1, columns=feature_names)

tf_idf_counter = df.T.sum(axis=1)