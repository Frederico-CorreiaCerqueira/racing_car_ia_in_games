import os
import csv

import pygame

from .abstract_car import AbstractCar
from utils.settings import RED_CAR


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (140, 200)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        self.last_saved_distances = None

    def move(self):
        super().move()
        self.center_x = self.x + self.IMG.get_width() // 2
        self.center_y = self.y + self.IMG.get_height() // 2

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def save_data(self, action):
        if not hasattr(self, "frame_count"):
            self.frame_count = 0

        self.frame_count += 1

        if self.frame_count % 10 != 0:
            return

        distances = self.get_radar_distances()
        #print(f"Distâncias: {distances}, Ação: {action}")

        # Verificar mudança significativa
        if self.last_saved_distances is None:
            # Primeira leitura — guarda logo
            #print("Primeira leitura, guardando distâncias.")
            self.last_saved_distances = distances
        else:
            # Comparação
            #print("Comparando distâncias com a última leitura.")
            diff = [abs(a - b) for a, b in zip(distances, self.last_saved_distances)]
            avg_diff = sum(diff) / len(diff)
            if avg_diff < 1e-2:
                return  # Não guarda se diferença muito pequena
            self.last_saved_distances = distances

        print(f"Distâncias: {distances}, Ação: {action}")
        self.last_saved_distances = distances

        row = distances + [action]
        os.makedirs("data", exist_ok=True)
        with open("data/dataset.csv", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

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
