import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import ast

# Load the CSV file
csv_file_path = "C:\\Users\\DELL\\Desktop\\USE\\AI-enabled-Reports-Analysis-Software\\Dataset.csv"
df = pd.read_csv(csv_file_path)

# Convert string representation of lists to actual lists
df['Embedding'] = df['Embedding'].apply(ast.literal_eval)

# Separate features (embeddings) and labels
X = df['Embedding'].tolist()
y = df['label'].tolist()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the multinomial logistic regression model
model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", classification_rep)
