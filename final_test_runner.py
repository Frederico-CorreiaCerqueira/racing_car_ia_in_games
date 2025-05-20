import os
import subprocess

print("[1/4] Recolher dados jogando com PlayerCar...")
subprocess.run(["python", "main.py"], check=True)

print("[2/4] Treinar modelo com Decision Tree...")
subprocess.run(["python", "train/dt_training.py"], check=True)

print("[3/4] Executar simulação com carro treinado e gravar trajetórias...")
subprocess.run(["python", "run_and_record.py"], check=True)

print("[4/4] Avaliar e comparar trajetórias...")
subprocess.run(["python", "evaluate_trajectory.py"], check=True)

print("Fluxo concluído!")
