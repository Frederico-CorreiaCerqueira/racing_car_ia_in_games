import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv("training_data.csv", header=None)

# Assume last column is the action
data.columns = [f"sensor_{i}" for i in range(data.shape[1] - 1)] + ["action"]
X = data.drop("action", axis=1)
y = data["action"]

# Encode labels
y_encoded = y.astype("category").cat.codes
label_map = dict(enumerate(y.astype("category").cat.categories))
pd.Series(label_map).to_csv("label_map.csv")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.2f}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", xticklabels=label_map.values(), yticklabels=label_map.values())
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

# Save model
joblib.dump(clf, "model.pkl")
print("Model saved as model.pkl")