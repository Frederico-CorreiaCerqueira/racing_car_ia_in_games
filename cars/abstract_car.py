import math
import numpy
import pygame
from utils.settings import CAR_SIZE, TRACK_BORDER_MASK, WIDTH, HEIGHT, TRACK_MASK
from utils.draw_helpers import blit_rotate_center


RADAR_ANGLES = [90, 45, -45, -90, 180]
MAX_RADAR_DISTANCE = 300

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
    """
    def get_radar_distances(self):
        # Nome de cada sensor para print
        sensor_names = ['Esquerda', 'Meio-Esquerda', 'Meio-Direita', 'Direita', 'Trás']

        distances = []
        for i, radar_angle in enumerate(RADAR_ANGLES):
            angle = math.radians(self.angle + radar_angle)
            dist = 0
            for dist in range(0, MAX_RADAR_DISTANCE, 2):
                x = int(self.x + math.sin(angle) * dist)
                y = int(self.y - math.cos(angle) * dist)

                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    if TRACK_MASK.get_at((x, y)) == 0:
                        break
                else:
                    break

            # Adiciona a distância medida
            distances.append(dist)

            # Print detalhado para ver as leituras
            print(f"Sensor {sensor_names[i]} ({radar_angle}°): {dist} pixels")

        return distances
    """
    def get_radar_distances(self):
        distances = []
        sensor_names = ['Esquerda', 'Meio-Esquerda', 'Meio-Direita', 'Direita', 'Trás']
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        for radar_angle in RADAR_ANGLES:
            angle = math.radians(self.angle + radar_angle)
            dx, dy = math.sin(angle), -math.cos(angle)

            dist = 0
            while dist < MAX_RADAR_DISTANCE:
                px, py = int(x + dx * dist), int(y + dy * dist)

                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    # Testa se encontrou um obstáculo (não-pista)
                    if TRACK_BORDER_MASK.get_at((px, py)) != 0:
                        break
                else:
                    break  # Fora dos limites

                dist += 2
            
            distances.append(dist)
        return distances

    def rotate(self, left=False, right=False):
        noise = numpy.random.normal(0, 0.5) 
        if left and right:
            return
        if left:
            self.angle += self.rotation_vel + noise
        elif right:
            self.angle -= self.rotation_vel + noise
        self.angle %= 360

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backwards(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel // 2)
        self.move()

    def move(self):
        noise = numpy.random.normal(0, 0.3)
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * (self.vel + noise)
        horizontal = math.sin(radians) * (self.vel + noise)
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

    def bounce(self):
        self.vel = -self.vel
        self.move()
