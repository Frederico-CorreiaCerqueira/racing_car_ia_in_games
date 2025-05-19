import joblib
import math
import numpy
import pygame
import pickle

from decision_tree.decision_tree import Action, Boolean
from .abstract_car import AbstractCar, MAX_RADAR_DISTANCE, RADAR_ANGLES
from settings import CAR_SIZE, GREEN_CAR, HEIGHT, RED, TRACK_MASK, WIDTH, YELLOW


class DecisionTreeTrainedCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)
    SENSOR_NAMES = ['left_far', 'left', 'center', 'right', 'right_far']

    # Corrigido: posições relativas dos sensores com base nos ângulos e distância máxima
    SENSOR_POS = [
        (
            MAX_RADAR_DISTANCE * math.sin(math.radians(angle)),  # eixo x (horizontal)
            -MAX_RADAR_DISTANCE * math.cos(math.radians(angle))  # eixo y (vertical)
        )
        for angle in RADAR_ANGLES
    ]

    def __init__(self, max_vel, rotation_vel, tree_path="./model/classifier.joblib"):
        super().__init__(max_vel, rotation_vel)
        self.DT = joblib.load(tree_path)
        self.update_sensors()

    def step(self):
        self.update_sensors()
        print("Esperadas pelo modelo:", self.DT.feature_names_in_)
        # Exemplo de construção do vetor de entrada para o modelo:
        valores = {self.SENSOR_NAMES[i] + "?": self.sensors[i][1] in (RED, YELLOW) for i in range(len(self.sensors))}
        action = self.DT.predict([valores])[0]
        getattr(self, action)()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02

    def draw_sensors(self, win):
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        alfa = math.radians(self.angle)
        mrot = numpy.array([[math.cos(alfa), -math.sin(alfa)], [math.sin(alfa), math.cos(alfa)]])
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
        mrot = numpy.array([[math.cos(alfa), -math.sin(alfa)], [math.sin(alfa), math.cos(alfa)]])
        pts = numpy.array(self.SENSOR_POS)
        npts = numpy.dot(pts, mrot)
        self.sensors = []
        for dx, dy in npts:
            sx, sy = int(dx + x), int(dy + y)
            color = TRACK_MASK.get_at((sx, sy)) if 0 <= sx < WIDTH and 0 <= sy < HEIGHT else None
            self.sensors.append(((sx, sy), color))

    # Ações
    def rotLeft(self):
        self.rotate(True, False)

    def rotRight(self):
        self.rotate(False, True)

    def accelerate(self):
        self.move_forward()

    def brake(self):
        self.move_backwards()
