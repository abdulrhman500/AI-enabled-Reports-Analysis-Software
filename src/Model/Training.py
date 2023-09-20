import pandas as pd 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from collections import Counter
# Load the dataset
data = pd.read_csv(r"")
print (data.label.value_counts())
# Define label encoder for the target variable
# 0 -> approved  1 -> pending 2 -> reject
le = LabelEncoder()
encoded_labels = le.fit_transform(data['label'])  # Encode the target variable
encoded_text = le.fit_transform(data['text'])  # Encode the text

# Reshape encoded_text to a 2D array with a single column
encoded_text = encoded_text.reshape(-1, 1)

# Define features (X) and target variable (y)
X = encoded_text
y = encoded_labels

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)

# Initialize the model
model = KNeighborsClassifier()

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_predict = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_predict)
print("Accuracy:", accuracy)
print(pd.crosstab(y_test,y_predict))
#-----------------------------------------

smote = SMOTE(k_neighbors=4)
X_train_smote, y_train_smote = smote.fit_resample(X_train,y_train)
print("Before SMOTE :" , Counter(y_train))
print("After SMOTE :" , Counter(y_train_smote))

#-----------------------------------------------
model.fit(X_train_smote,y_train_smote)
y_predict = model.predict(X_test)
print("Accuracy : " , accuracy_score(y_test,y_predict))
print(pd.crosstab(y_test,y_predict))


precision = precision_score(y_test, y_predict, average='weighted')
recall = recall_score(y_test, y_predict, average='weighted')
f1 = f1_score(y_test, y_predict, average='weighted')
roc_auc = roc_auc_score(y_test, model.predict_proba(X_test), average='macro', multi_class='ovr')


print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)
print("ROC AUC:", roc_auc)