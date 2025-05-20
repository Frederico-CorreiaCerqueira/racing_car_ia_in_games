import joblib
import math
import numpy
import pygame
import pandas as pd

from cars.abstract_car import AbstractCar, MAX_RADAR_DISTANCE, RADAR_ANGLES
from settings import (
    CAR_SIZE, GREEN_CAR, HEIGHT, RED, TRACK_MASK, WIDTH, YELLOW,
    images, WIN, FPS
)


class DecisionTreeTrainedCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    SENSOR_POS = [
        (
            MAX_RADAR_DISTANCE * math.sin(math.radians(angle)),
            -MAX_RADAR_DISTANCE * math.cos(math.radians(angle))
        )
        for angle in RADAR_ANGLES
    ]

    def __init__(self, max_vel, rotation_vel, tree_path="model/classifier.joblib"):
        super().__init__(max_vel, rotation_vel)
        self.DT = joblib.load(tree_path)
        self.update_sensors()

    def step(self):
        self.update_sensors()

        # Extrai os valores brutos de cor nos sensores (RED/YELLOW = obstáculo)
        valores = [
            self.sensors[i][1] in (RED, YELLOW)
            for i in range(len(self.sensors))
        ]

        # Cria DataFrame compatível com as colunas do treino (s1 a s5)
        df = pd.DataFrame([valores], columns=[f"s{i+1}" for i in range(5)])

        # Prediz a ação
        action = self.DT.predict(df)[0]

        # Mapeia ação para método correspondente
        action_map = {
            "w": self.accelerate,
            "a": self.rotLeft,
            "d": self.rotRight,
            "s": self.brake,
            "accelerate": self.accelerate,
            "rotLeft": self.rotLeft,
            "rotRight": self.rotRight,
            "brake": self.brake
        }

        act_fn = action_map.get(action)
        if act_fn:
            act_fn()
        else:
            print(f"Ação inválida do modelo: {action}")

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02

    def draw_sensors(self, win):
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        alfa = math.radians(self.angle)
        mrot = numpy.array([
            [math.cos(alfa), -math.sin(alfa)],
            [math.sin(alfa), math.cos(alfa)]
        ])
        pts = numpy.array(self.SENSOR_POS)
        npts = numpy.dot(pts, mrot)
        for i in npts:
            px, py = int(i[0] + x), int(i[1] + y)
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                pygame.draw.circle(win, TRACK_MASK.get_at((px, py)), (px, py), 2, 2)

    def draw(self, win):
        super().draw(win)
        self.draw_sensors(win)

    def update_sensors(self):
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        alfa = math.radians(self.angle)
        mrot = numpy.array([
            [math.cos(alfa), -math.sin(alfa)],
            [math.sin(alfa), math.cos(alfa)]
        ])
        pts = numpy.array(self.SENSOR_POS)
        npts = numpy.dot(pts, mrot)
        self.sensors = []
        for dx, dy in npts:
            sx, sy = int(dx + x), int(dy + y)
            color = TRACK_MASK.get_at((sx, sy)) if 0 <= sx < WIDTH and 0 <= sy < HEIGHT else None
            self.sensors.append(((sx, sy), color))

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
