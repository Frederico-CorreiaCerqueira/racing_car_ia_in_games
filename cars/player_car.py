import math

import pygame
from .abstract_car import MAX_RADAR_DISTANCE, RADAR_ANGLES, AbstractCar
from settings import HEIGHT, RED_CAR, TRACK_MASK, WIDTH
import os
import csv

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def draw(self, win):
        super().draw(win)
        distances = self.get_radar_distances()
        
        #self.draw_radar_lines(win)

        """
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
            pygame.draw.circle(win, (0, 255, 0), (end_x, end_y), 4)"""

    def save_data(self, action):
        print("Action:", action)
        distances = self.get_radar_distances()
        row = distances + [action]

        os.makedirs("data", exist_ok=True)
        with open("data/dataset.csv", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)