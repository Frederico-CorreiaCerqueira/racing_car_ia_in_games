import math
import numpy
import pygame
from settings import CAR_SIZE, WIDTH, HEIGHT, TRACK_MASK
from utils.draw_helpers import blit_rotate_center

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left and right:
            return
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        self.angle %= 360

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backwards(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel // 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
