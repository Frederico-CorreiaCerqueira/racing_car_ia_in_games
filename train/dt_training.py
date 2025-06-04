from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report
import pandas as pd
import joblib
import os
from collections import Counter
from imblearn.over_sampling import RandomOverSampler
import matplotlib.pyplot as plt

# Nomes das colunas (sensores + ação)
col_names = ['s1', 's2', 's3', 's4', 's5', 'action']
df = pd.read_csv("data/dataset.csv", header=None, names=col_names)

# Limpeza do dataset
df = df.dropna()
df = df[df['action'].isin(['w', 'a', 'd', 's'])]
df['action'] = df['action'].astype(str)
df = df.drop_duplicates()

print("Distribuição das ações:")
print(df['action'].value_counts())

# Define X e y
X = df[["s1", "s2", "s3", "s4", "s5"]]
y = df['action']

# Balanceamento com oversampling
ros = RandomOverSampler(random_state=42)
X_balanced, y_balanced = ros.fit_resample(X, y)

print("Antes do oversampling:", Counter(y))
print("Depois do oversampling:", Counter(y_balanced))

# Divide treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X_balanced, y_balanced, stratify=y_balanced, test_size=0.2, random_state=42)


"""Modelos de Classificação utilizados, para comparação"""

# MODELO 1: Random Forest
clf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)

# MODELO 2: Rede Neural simples (MLP)
#clf = MLPClassifier(hidden_layer_sizes=(20,), max_iter=500, random_state=42)

# MODELO 3: Decision Tree clássica (ajustada para melhor generalização)
#clf = DecisionTreeClassifier(max_depth=10, min_samples_split=4, min_samples_leaf=5, random_state=42)


clf.fit(X_train, y_train)

# Avaliação
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)
print(classification_report(y_test, y_pred))

# Matriz de confusão
cm = confusion_matrix(y_test, y_pred, labels=["w", "a", "d", "s"])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["w", "a", "d", "s"])
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

# Salvar o modelo
os.makedirs("model", exist_ok=True)
joblib.dump(clf, "model/classifier.joblib")