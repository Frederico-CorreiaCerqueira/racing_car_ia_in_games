import math
import pygame
import os
import csv

from .abstract_car import MAX_RADAR_DISTANCE, RADAR_ANGLES, AbstractCar
from utils.settings import RED_CAR, TRACK_MASK, TRACK_BORDER_MASK, TRACK, WIDTH, HEIGHT


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        self.center_x = self.x + self.IMG.get_width() // 2
        self.center_y = self.y + self.IMG.get_height() // 2

    def move(self):
        super().move()
        self.center_x = self.x + self.IMG.get_width() // 2
        self.center_y = self.y + self.IMG.get_height() // 2

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def move_player(self):
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_a]:
            self.rotate(left=True)
            self.save_data("a")
        if keys[pygame.K_d]:
            self.rotate(right=True)
            self.save_data("d")
        if keys[pygame.K_w]:
            moved = True
            self.move_forward()
            self.save_data("w")
        if keys[pygame.K_s]:
            moved = True
            self.move_backwards()
            self.save_data("s")
        if not moved:
            self.reduce_speed()

    def draw_radar_lines(self, win):
        for radar_angle in RADAR_ANGLES:
            angle = math.radians(self.angle + radar_angle + 90)
            dist = 0
            end_x, end_y = self.center_x, self.center_y

            for d in range(0, MAX_RADAR_DISTANCE, 2):
                dx = int(self.center_x + math.cos(angle) * d)
                dy = int(self.center_y - math.sin(angle) * d)

                if 0 <= dx < WIDTH and 0 <= dy < HEIGHT:
                    if TRACK_BORDER_MASK.get_at((dx, dy)) != 0:
                        break
                else:
                    break
                dist = d
                end_x, end_y = dx, dy

            pygame.draw.line(win, (255, 0, 0), (int(self.center_x), int(self.center_y)), (end_x, end_y), 2)

            if 0 <= end_x < WIDTH and 0 <= end_y < HEIGHT:
                r, g, b = TRACK.get_at((end_x, end_y))[:3]
                is_grass = g > r + 20 and g > b + 20 and g > 100
                is_border = r > 100 and g < 100 and b < 100
                is_off_track = is_grass or is_border
            else:
                is_off_track = True

            color = (255, 0, 0) if is_off_track else (0, 255, 0)
            pygame.draw.circle(win, color, (end_x, end_y), 4)

    def draw(self, win):
        super().draw(win)
       # self.draw_radar_lines(win)

    def save_data(self, action):
        if not hasattr(self, "frame_count"):
            self.frame_count = 0

        self.frame_count += 1

        if self.frame_count % 5 != 0:
            return

        distances = self.get_radar_distances()
       # print(distances)
        row = distances + [action]
        os.makedirs("data", exist_ok=True)
        with open("data/dataset.csv", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
