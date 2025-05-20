import os
import subprocess

print("[1/3] Recolher dados jogando com PlayerCar...")
subprocess.run(["python", "main.py"], check=True)

print("[2/3] Treinar modelo com Decision Tree...")
subprocess.run(["python", "train/dt_training.py"], check=True)

print("[3/3] Avaliar e comparar trajetórias...")
subprocess.run(["python", "evaluate_trajectory.py"], check=True)

print("Concluído!")
