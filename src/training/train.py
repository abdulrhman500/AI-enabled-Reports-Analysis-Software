import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tf_idf import apply_tf_idf , preprocess_document
# from USE import apply_USE 
from Data import Data
from sklearn.metrics import f1_score, accuracy_score, classification_report
from imblearn.over_sampling import SMOTE



def read_csv_data(csv_file):
    data = pd.read_csv(csv_file)
    names = data['name'].tolist()
    labels = data['label'].tolist()
    texts = data['text'].tolist()
    return names, labels, texts

csv_file = 'Dataset.csv'
names, labels, texts = read_csv_data(csv_file)


def addToData1(names, labels, texts, data_obj, vectorization_technique):
    for name, label, text in zip(names, labels, texts):
        vector = vectorization_technique(text.strip()).numpy().tolist()
        data_obj.add_data(name.strip(), vector, label.strip())
    return data_obj

def addToData2(names, labels, texts,data_obj,preprocess_document=preprocess_document ,vectorization_technique=apply_tf_idf):
    temp = []
    for text in texts:
        text = preprocess_document(text.strip())    
        temp.append(text)
    texts = temp
        
    vectors = vectorization_technique(texts)
    for name, label, vector in zip(names, labels, vectors):
        data_obj.add_data(name.strip(), vector, label.strip())
    return data_obj

obj = Data()
# obj1 = addToData1(names, labels, texts, obj, apply_USE) 
# obj =  Data()
obj2 = addToData2(names, labels, texts, obj, preprocess_document, apply_tf_idf)
# print("*********** Obj 1 *****************")
# print(obj1)
print("*********** Obj 2 ******************")
print(obj2)

  
# Load your dataset
print("****\n",obj2.col_document_vector,"\n****")
X = obj2.get_column(obj2.col_document_vector)
y = obj2.get_column(obj2.col_decision)


smote = SMOTE()
X_sm , y_sm = smote.fit_resample(X,y)



X_train, X_test, y_train, y_test = train_test_split(X_sm, y_sm, test_size=0.2, random_state=42)











model = LogisticRegression()
# model.fit(X_train, y_train)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

f1 = f1_score(y_test, y_pred, average='weighted')


print("F1-score:", f1)
print("Accuracy:", accuracy)

class_report = classification_report(y_test, y_pred)
print("Classification Report:\n", class_report)
