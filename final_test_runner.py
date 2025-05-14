import os
import subprocess

print("[1/3] Treinar modelo com scikit-learn...")
subprocess.run(["python", "train_model.py"], check=True)

print("[2/3] Correr simulação e gravar trajetórias...")
subprocess.run(["python", "run_and_record.py"], check=True)

print("[3/3] Avaliar trajetórias com gráfico de erro...")
subprocess.run(["python", "evaluate_trajectory.py"], check=True)

print("Teste final completo!")