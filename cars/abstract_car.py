import math
import numpy
import pygame
from utils.settings import WIDTH, HEIGHT, TRACK_MASK, TRACK_BORDER_MASK
from utils.draw_helpers import blit_rotate_center

RADAR_ANGLES = [90, 45, 0, -45, -90]
MAX_RADAR_DISTANCE = 300
ORIGIN_OFFSET = 0  # distância do centro até ao para-choques (ajustável)

class AbstractCar:
    """
    Classe abstrata que define o comportamento básico dos carros no jogo.

    Esta classe serve como base para carros controlados manualmente ou por agentes automatizados.
    Inclui funcionalidades para movimento, rotação com ruído (simulando imperfeições reais),
    detecção de distâncias via sensores (radares), deteção de colisões com a pista e reinício
    da posição. Pode ser estendida para implementar comportamento mais específico.

    Atributos principais:
    - max_vel: velocidade máxima permitida.
    - vel: velocidade atual.
    - rotation_vel: velocidade de rotação.
    - angle: ângulo atual do carro.
    - x, y: coordenadas atuais do carro no ecrã.
    - acceleration: aceleração usada para mover o carro.

    Métodos principais:
    - move_forward / move_backwards: acelera ou trava o carro.
    - rotate: gira o carro com ruído adicionado.
    - move: aplica o movimento segundo o ângulo e velocidade.
    - get_radar_distances: retorna distâncias medidas pelos sensores do carro.
    - collide: verifica colisão com uma máscara (pista ou obstáculos).
    - bounce: simula o efeito de bouncing ao colidir.
    - reset: reinicia a posição e estado do carro.
    - draw: desenha o carro na janela do jogo.
"""


    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def get_radar_distances(self):
        distances = []
        center_x = self.x + self.img.get_width() // 2
        center_y = self.y + self.img.get_height() // 2

        for radar_angle in RADAR_ANGLES:
            angle = math.radians(self.angle + radar_angle + 90)

            # Origem do sensor: frente do carro (para-choques)
            start_x = center_x + math.cos(angle) * ORIGIN_OFFSET
            start_y = center_y - math.sin(angle) * ORIGIN_OFFSET

            dist = 0
            for d in range(0, MAX_RADAR_DISTANCE, 2):
                dx = int(start_x + math.cos(angle) * d)
                dy = int(start_y - math.sin(angle) * d)

                if 0 <= dx < WIDTH and 0 <= dy < HEIGHT:
                    if TRACK_MASK.get_at((dx, dy)) == 0 or TRACK_BORDER_MASK.get_at((dx, dy)) != 0:
                        break
                else:
                    break

                dist = d

            distances.append(float(dist))

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
        #self.angle = 0
        self.angle = getattr(self, "start_angle", self.angle)
        self.vel = 0

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def bounce(self):
        self.vel = -self.vel
        self.move()