import pandas as pd 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE
from collections import Counter

# Load the dataset
data = pd.read_csv(r"d:\University\semesters\Summer 2023\AI-enabled-Reports-Analysis-Software\src\Model\Dataset.csv")

# Define label encoder for the target variable
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

# Apply SMOTE to the training data
smote = SMOTE()
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# Initialize the model
model = KNeighborsClassifier()

# Train the model on the SMOTE-resampled data
model.fit(X_train_smote, y_train_smote)

# Make predictions
y_predict = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_predict)
print("Accuracy:", accuracy)

# Print cross-tabulation
print(pd.crosstab(y_test, y_predict))
