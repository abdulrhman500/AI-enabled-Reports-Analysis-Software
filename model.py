import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import ast

# Load the CSV file
csv_file_path = "C:\\Users\\DELL\\Desktop\\USE\\AI-enabled-Reports-Analysis-Software\\Dataset.csv"
df = pd.read_csv(csv_file_path)

df['Embedding'] = df['Embedding'].apply(ast.literal_eval)

X = df['Embedding'].tolist()
y = df['label'].tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

oversampler = SMOTE(sampling_strategy={'Reject': 1000, 'Pending': 1000})
X_train_resampled, y_train_resampled = oversampler.fit_resample(X_train, y_train)

undersampler = RandomUnderSampler(sampling_strategy={'Approved': 100})
X_train_final, y_train_final = undersampler.fit_resample(X_train_resampled, y_train_resampled)

model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
model.fit(X_train_final, y_train_final)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", classification_rep)
