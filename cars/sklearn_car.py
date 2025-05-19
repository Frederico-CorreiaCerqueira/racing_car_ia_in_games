import joblib
import os
from .abstract_car import AbstractCar
from settings import GREEN_CAR
import numpy as np
import pandas as pd

class SklearnCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        if os.path.exists("model.pkl"):
            self.model = joblib.load("model.pkl")
            self.label_map = pd.read_csv("label_map.csv", index_col=0, header=None).squeeze().to_dict()
            self.inv_label_map = {v: k for k, v in self.label_map.items()}
        else:
            print("⚠️ model.pkl not found! SklearnCar disabled.")
            self.model = None

    def step(self):
        if self.model is None:
            return
        sensor_values = self.get_radar_distances()
        X = pd.DataFrame([sensor_values], columns=[f"sensor_{i}" for i in range(len(sensor_values))])
        prediction = self.model.predict(X)[0]
        action = self.label_map[prediction] if prediction in self.label_map else prediction

        if action == "accelerate":
            self.move_forward()
        elif action == "brake":
            self.move_backwards()
        elif action == "rotLeft":
            self.rotate(left=True)
        elif action == "rotRight":
            self.rotate(right=True)

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02