import math
import numpy as np
import pygame

from decision_tree.decision_tree import Action, Boolean
from .abstract_car import AbstractCar
from settings import (
    CAR_SIZE, GREEN_CAR, HEIGHT, TRACK_BORDER_MASK, WIDTH
)

# Define árvore de decisão simples
acc = Action("accelerate")
rl = Action('rotLeft')
rr = Action('rotRight')
br = Action('brake')
right = Boolean("east?", rl, acc)
left = Boolean("west?", rr, right)
rightb = Boolean("east?", rl, br)
leftb = Boolean("west?", rr, rightb)
north = Boolean("north?", leftb, left)
decisionTreeSimple = north

class DTSimpleCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)
    SENSOR_POS = [(0, -50), (-20, -30), (20, -30), (0, 40)]
    SENSOR_NAMES = ['north', "west", "east", "south"]
    DT = decisionTreeSimple

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        self.update_sensors()
        #self.sensors [WHITE, WHITE, WHITE, WHITE]
        # deveria ser feito o UPDATE_SENSORS para termos os primeiros valores

    def step(self):
        self.update_sensors()
        valores = dict()
        for i in range(4):
            obstacle = self.sensors[i][1]
            valores[self.SENSOR_NAMES[i] + "?"] = obstacle
        # aqui teremos que devolver o dicionário com os nomes
        action = self.DT.decide(valores)
        #print(valores,'------------------------->',action)
        eval('self.' + action + '()')

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02

    def draw(self, win):
        super().draw(win)
        self.draw_sensors(win)

    def draw_sensors(self, win):
        for pos, _ in self.sensors:
            px, py = int(pos[0]), int(pos[1])
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                pygame.draw.circle(win, (0, 0, 0), (px, py), 2)

    def update_sensors(self):
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        alfa = math.radians(self.angle)
        mrot = np.array([
            [math.cos(alfa), -math.sin(alfa)],
            [math.sin(alfa), math.cos(alfa)]
        ])
        pts = np.array(self.SENSOR_POS)
        npts = np.dot(pts, mrot)
        self.sensors = []
        for dx, dy in npts:
            px, py = int(x + dx), int(y + dy)
            is_obstacle = False
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                is_obstacle = TRACK_BORDER_MASK.get_at((px, py)) != 0
            self.sensors.append(((px, py), is_obstacle))

    # Ações
    def rotLeft(self):
        self.rotate(left=True)

    def rotRight(self):
        self.rotate(right=True)

    def accelerate(self):
        self.move_forward()

    def brake(self):
        self.move_backwards()
