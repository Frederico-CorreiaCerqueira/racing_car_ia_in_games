import joblib
import math
import numpy
import pygame
import pandas as pd

from cars.abstract_car import AbstractCar
from settings import (
    GREEN_CAR, TRACK_MASK, TRACK_BORDER_MASK,
    WIDTH, HEIGHT, CAR_SIZE, FPS, images, WIN
)

RADAR_ANGLES = [-60, -30, 0, 30, 60]
MAX_RADAR_DISTANCE = 150
SENSOR_NAMES = ['s1', 's2', 's3', 's4', 's5']


class DecisionTreeTrainedCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, tree_path="model/classifier.joblib"):
        super().__init__(max_vel, rotation_vel)
        self.DT = joblib.load(tree_path)
        self.update_sensors()

    def step(self):
        self.update_sensors()
        sensor_values = [dist for (_, dist) in self.sensors]

        df = pd.DataFrame([sensor_values], columns=SENSOR_NAMES)
        predicted_key = self.DT.predict(df)[0]
       # print(f"Sensors: {sensor_values} → Predicted Action: {predicted_key}")

        action_map = {
            "w": self.accelerate,
            "a": self.rotLeft,
            "d": self.rotRight,
            "s": self.brake
        }

        if predicted_key in action_map:
            action_map[predicted_key]()
        else:
            print(f"Ação inválida prevista: {predicted_key}")

    def update_sensors(self):
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        self.sensors = []

        for angle_offset in RADAR_ANGLES:
            angle = math.radians(self.angle + angle_offset)
            dist = 0
            for d in range(0, MAX_RADAR_DISTANCE, 2):
                sx = int(x + math.sin(angle) * d)
                sy = int(y - math.cos(angle) * d)

                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    if TRACK_MASK.get_at((sx, sy)) == 0:
                        break
                else:
                    break
                dist = d

            self.sensors.append(((sx, sy), dist))

    def draw_sensors(self, win):
        for (pos, dist) in self.sensors:
            if 0 <= pos[0] < WIDTH and 0 <= pos[1] < HEIGHT:
                pygame.draw.circle(win, (0, 255, 0), (int(pos[0]), int(pos[1])), 3, 1)

    def draw(self, win):
        super().draw(win)
        self.draw_sensors(win)

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02

    def rotLeft(self):
        self.rotate(True, False)

    def rotRight(self):
        self.rotate(False, True)

    def accelerate(self):
        self.move_forward()

    def brake(self):
        self.move_backwards()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Decision Tree Trained Car")
    clock = pygame.time.Clock()

    car = DecisionTreeTrainedCar(max_vel=3, rotation_vel=3)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for img, pos in images:
            WIN.blit(img, pos)

        car.step()

        if car.collide(TRACK_BORDER_MASK):
            print("COLISÃO COM A BORDA!")
            car.bounce()
        else:
            print("Sem colisão")

        car.draw(WIN)
        pygame.display.update()

    pygame.quit()
