import joblib
import math
import numpy
import pygame
import pandas as pd

from .abstract_car import AbstractCar
from settings import CAR_SIZE, GREEN_CAR, HEIGHT, TRACK_MASK, WIDTH, FPS, TRACK

RADAR_ANGLES = [-60, -30, 0, 30, 60]
MAX_RADAR_DISTANCE = 150
SENSOR_NAMES = ['s1', 's2', 's3', 's4', 's5']


class DecisionTreeTrainedCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, model_path="model/classifier.joblib"):
        super().__init__(max_vel, rotation_vel)
        self.DT = joblib.load(model_path)
        
        self.center_x = self.x + self.IMG.get_width() // 2
        self.center_y = self.y + self.IMG.get_height() // 2
        self.update_sensors()

    def move(self):
        super().move()
        
        self.center_x = self.x + self.IMG.get_width() // 2
        self.center_y = self.y + self.IMG.get_height() // 2

    def step(self):
        self.update_sensors()
        sensor_values = [dist for (_, dist) in self.sensors]
        df = pd.DataFrame([sensor_values], columns=SENSOR_NAMES)

        predicted_key = self.DT.predict(df)[0]

       # print(f"Radares: {sensor_values} → Ação prevista: {predicted_key}")

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


    def update_sensors(self):
        self.sensors = []

        for angle_offset in RADAR_ANGLES:
            angle = math.radians(self.angle + angle_offset)
            dist = 0
            end_x, end_y = self.center_x, self.center_y  # Inicia no centro do carro
            
            for d in range(0, MAX_RADAR_DISTANCE, 2):
                dx = int(self.center_x + math.sin(angle) * d)
                dy = int(self.center_y - math.cos(angle) * d)

                if 0 <= dx < WIDTH and 0 <= dy < HEIGHT:
                    if TRACK_MASK.get_at((dx, dy)) == 0:
                        break
                else:
                    break
                dist = d
                end_x, end_y = dx, dy

            self.sensors.append(((end_x, end_y), dist))

    def draw_sensors(self, win):
        
        for (pos, dist) in self.sensors:
            end_x, end_y = pos
            pygame.draw.line(win, (255, 0, 0), (int(self.center_x), int(self.center_y)), (end_x, end_y), 2)
        
        
        for (pos, dist) in self.sensors:
            dx, dy = int(pos[0]), int(pos[1])

            if 0 <= dx < WIDTH and 0 <= dy < HEIGHT:
                r, g, b = TRACK.get_at((dx, dy))[:3]
                is_grass = g > r + 20 and g > b + 20 and g > 100
                is_border = r > 100 and g < 100 and b < 100
                is_off_track = is_grass or is_border
            else:
                is_off_track = True

            color = (255, 0, 0) if is_off_track else (0, 255, 0)
            pygame.draw.circle(win, color, (dx, dy), 4)

    def draw(self, win):
        super().draw(win)
     #   self.draw_sensors(win)

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02
       
        self.center_x = self.x + self.IMG.get_width() // 2
        self.center_y = self.y + self.IMG.get_height() // 2

    def rotLeft(self):
        self.rotate(left=True)

    def rotRight(self):
        self.rotate(right=True)

    def accelerate(self):
        self.move_forward()

    def brake(self):
        self.move_backwards()