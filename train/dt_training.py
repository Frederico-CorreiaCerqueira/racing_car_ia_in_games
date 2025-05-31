"""from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib 
import os

# Carrega os dados
col_names = ['s1', 's2', 's3', 's4', 's5', 'action']
df = pd.read_csv("data/dataset.csv",header=None, names=col_names)
print(df['action'].value_counts())
X = df[['s1', 's2', 's3', 's4', 's5']]  # sensores
y = df['action']                       # ações

# Divide treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Treina o classificador
clf = DecisionTreeClassifier(max_depth=5)
clf.fit(X_train, y_train)

# Avalia
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

# Salva o modelo
os.makedirs("model", exist_ok=True)
joblib.dump(clf, "model/classifier.joblib")"""


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib
import os
from collections import Counter

# Importa a biblioteca para balanceamento
from imblearn.over_sampling import RandomOverSampler

# Carrega os dados
col_names = ['s1', 's2', 's3', 's4', 's5', 'action']
df = pd.read_csv("data/dataset.csv", header=None, names=col_names)
print(df['action'].value_counts())

# Define features e rótulos
X = df[['s1', 's2', 's3', 's4', 's5']]
y = df['action']

# Balanceia as classes usando RandomOverSampler
ros = RandomOverSampler(random_state=42)
X_balanced, y_balanced = ros.fit_resample(X, y)

# Divide treino/teste nos dados balanceados
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, stratify=y_balanced, test_size=0.2, random_state=42)
#X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Treina o classificador
clf = DecisionTreeClassifier(max_depth=5)
clf.fit(X_train, y_train)

print("Antes do oversampling:", Counter(y))
print("Depois do oversampling:", Counter(y_balanced))

# Avalia
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

# Salva o modelo
os.makedirs("model", exist_ok=True)
joblib.dump(clf, "model/classifier.joblib")
