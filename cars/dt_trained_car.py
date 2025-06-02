import joblib
import math
import pygame
import pandas as pd

from .abstract_car import AbstractCar
from utils.settings import GREEN_CAR, TRACK, WIDTH, HEIGHT, TRACK_MASK, TRACK_BORDER_MASK
from .abstract_car import RADAR_ANGLES, MAX_RADAR_DISTANCE

SENSOR_NAMES = ['s1', 's2', 's3', 's4', 's5']


class DecisionTreeTrainedCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (180, 200)

    def __init__(self, max_vel, rotation_vel, model_path="model/classifier.joblib"):
        super().__init__(max_vel, rotation_vel)
        self.DT = joblib.load(model_path)
        self.sensors = []

    def step(self):
        self.sensors = self.get_radar_distances()
        df = pd.DataFrame([self.sensors], columns=SENSOR_NAMES)

        predicted_key = self.DT.predict(df)[0]

        action_map = {
            "w": self.accelerate,
            "a": self.rotLeft,
            "d": self.rotRight,
            "s": self.brake
        }

        if predicted_key in action_map:
            action_map[predicted_key]()
        else:
            print("Ação inválida prevista:", predicted_key)

    def draw_sensors(self, win):
        center_x = self.x + self.img.get_width() // 2
        center_y = self.y + self.img.get_height() // 2

        for radar_angle in RADAR_ANGLES:
            angle = math.radians(self.angle + radar_angle + 90)
            dist = 0
            end_x, end_y = center_x, center_y

            for d in range(0, MAX_RADAR_DISTANCE, 2):
                dx = int(center_x + math.cos(angle) * d)
                dy = int(center_y - math.sin(angle) * d)

                if 0 <= dx < WIDTH and 0 <= dy < HEIGHT:
                    if TRACK_BORDER_MASK.get_at((dx, dy)) != 0:
                        break
                else:
                    break
                dist = d
                end_x, end_y = dx, dy

            pygame.draw.line(win, (255, 0, 0), (center_x, center_y), (end_x, end_y), 2)

            if 0 <= end_x < WIDTH and 0 <= end_y < HEIGHT:
                is_off_track = TRACK_MASK.get_at((end_x, end_y)) == 0
            else:
                is_off_track = True

            color = (255, 0, 0) if is_off_track else (0, 255, 0)
            pygame.draw.circle(win, color, (end_x, end_y), 4)

    def draw(self, win):
        super().draw(win)
      #  self.draw_sensors(win)

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02

    def rotLeft(self):
        self.rotate(left=True)

    def rotRight(self):
        self.rotate(right=True)

    def accelerate(self):
        self.move_forward()

    def brake(self):
        self.move_backwards()


