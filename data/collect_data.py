import csv
import os

def save_data(sensor_vals, action):
    row = sensor_vals + [action]
    os.makedirs("data", exist_ok=True)
    with open("data/dataset.csv", mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)