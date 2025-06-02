import math
import pygame
from utils.path import PATH
from .abstract_car import AbstractCar
from utils.settings import GREEN_CAR


class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)
    
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path=path
        self.current_point=0
        self.vel=self.max_vel
             
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = (1 if x_diff<0 else -1)*math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360
            
        elif difference_in_angle <= -180:
            difference_in_angle += 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1
            
    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()
            
    def draw_points(self,win):
        for point in self.path:
            pygame.draw.circle(win,(255,0,0),point,5)
        
    def draw(self,win):
        super().draw(win)
        self.draw_points(win)
    
    def step(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

