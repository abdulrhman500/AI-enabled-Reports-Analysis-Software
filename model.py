import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
import ast

# Load the CSV file
csv_file_path = "C:\\Users\\DELL\\Desktop\\USE\\AI-enabled-Reports-Analysis-Software\\Dataset.csv"
df = pd.read_csv(csv_file_path)

df['Embedding'] = df['Embedding'].apply(ast.literal_eval)

X = df['Embedding'].tolist()
y = df['label'].tolist()

# Apply SMOTE oversampling to the entire dataset
oversampler = SMOTE(sampling_strategy={'Reject': 165, 'Pending': 165})
X_resampled, y_resampled = oversampler.fit_resample(X, y)

# Split the resampled data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

model = LogisticRegression(solver='lbfgs', max_iter=1300)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", classification_rep)
