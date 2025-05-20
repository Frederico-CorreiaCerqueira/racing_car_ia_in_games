import joblib
import math
import numpy
import pygame
import pandas as pd

from cars.abstract_car import AbstractCar, RADAR_ANGLES, MAX_RADAR_DISTANCE
from settings import (
    CAR_SIZE, GREEN_CAR, WIDTH, HEIGHT,
    images, WIN, FPS, TRACK_MASK
)


class DecisionTreeTrainedCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, tree_path="model/classifier.joblib"):
        super().__init__(max_vel, rotation_vel)
        self.DT = joblib.load(tree_path)

    def step(self):
        sensor_values = self.get_radar_distances()

      # print(f"Sensors: {sensor_values}")

        df = pd.DataFrame([sensor_values], columns=["s1", "s2", "s3", "s4", "s5"])

        predicted_key = self.DT.predict(df)[0]
     #  print(f"Predicted action: {predicted_key}")

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

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02

    def draw(self, win):
        super().draw(win)
        self.draw_radar_lines(win)

    def draw_radar_lines(self, win):
        for radar_angle in RADAR_ANGLES:
            angle = math.radians(self.angle + radar_angle)
            dist = 0
            for d in range(0, MAX_RADAR_DISTANCE, 2):
                x = int(self.x + math.sin(angle) * d)
                y = int(self.y - math.cos(angle) * d)

                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    if TRACK_MASK.get_at((x, y)) == 0:
                        break
                else:
                    break
                dist = d

            end_x = int(self.x + math.sin(angle) * dist)
            end_y = int(self.y - math.cos(angle) * dist)
            pygame.draw.line(win, (255, 0, 0), (self.x, self.y), (end_x, end_y), 2)
            pygame.draw.circle(win, (0, 255, 0), (end_x, end_y), 4)

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
        car.draw(WIN)
        pygame.display.update()

    pygame.quit()
