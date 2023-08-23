import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import numpy as np
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

sentences = ["I ate dinner.", 
       "We had a three-course meal.", 
       "Brad came to dinner with us.",
       "He loves fish tacos.",
       "In the end, we all felt like we ate too much.",
       "We all agreed; it was a magnificent evening."]
# Tokenization of each document
tokenized_sent = []
for s in sentences:
    tokenized_sent.append(word_tokenize(s.lower()))
# print(tokenized_sent)

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

tagged_data = [TaggedDocument(d, [i]) for i, d in enumerate(tokenized_sent)]

model = Doc2Vec(tagged_data, vector_size = 20, window = 2, min_count = 1, epochs = 100)

test_doc = word_tokenize("I had pizza and pasta".lower())
test_doc_vector = model.infer_vector(test_doc)
ans = model.docvecs.most_similar(positive = [test_doc_vector])
print(ans)