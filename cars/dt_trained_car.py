import joblib
import math
import pygame
import pandas as pd
import csv

from .abstract_car import AbstractCar
from utils.settings import GREEN_CAR, WIDTH, HEIGHT, TRACK_MASK, TRACK_BORDER_MASK
from .abstract_car import RADAR_ANGLES, MAX_RADAR_DISTANCE

SENSOR_NAMES = ['s1', 's2', 's3', 's4', 's5']


class DecisionTreeTrainedCar(AbstractCar):
    """
    Classe que representa um carro autónomo controlado por um modelo treinado.

    Este carro utiliza um classificador treinado (carregado de um ficheiro `.joblib`) para prever
    ações com base nas leituras dos sensores frontais. O modelo decide entre acelerar, travar e virar
    à esquerda ou direita com base nas distâncias aos obstáculos captadas pelos sensores.

    Foi o principal agente utilizado durante as simulações, e baseia-se num modelo treinado com
    dados reais recolhidos, por outros carros. Além disso, a classe tem suporte para
    continuação da recolha de dados, permitindo armazenar novas observações e previsões para
    futuras melhorias do modelo.

    Atributos:
    - DT: o classificador Random Decision Tree carregado.
    - sensors: lista das leituras atuais dos sensores.
    - record: booleano que ativa a gravação de dados para ficheiro CSV.

    Métodos principais:
    - step: executa uma ação com base na previsão do modelo e (se ativado) grava os dados num CSV.
    - draw_sensors: desenha visualmente os sensores.
    - draw: desenha o carro na janela.
    - next_level: reposiciona o carro e ajusta a velocidade para simular progressão de dificuldade.
    - rotLeft / rotRight / accelerate / brake: executam as ações previstas pelo modelo.

    Este agente é também capaz de gerar mais dados para continuar a treinar e afinar o modelo ao longo do tempo.
    """

    IMG = GREEN_CAR
    START_POS = (180, 200)

    def __init__(self, max_vel, rotation_vel, model_path="model/classifier.joblib", record=False):
        super().__init__(max_vel, rotation_vel)
        self.DT = joblib.load(model_path)
        self.sensors = []
        self.record = record

    def step(self):
        self.sensors = self.get_radar_distances()
        df = pd.DataFrame([self.sensors], columns=SENSOR_NAMES)

        predicted_key = self.DT.predict(df)[0]

        # Executa a ação prevista
        action_map = {
            "w": self.accelerate,
            "a": self.rotLeft,
            "d": self.rotRight,
            "s": self.brake
        }

        if predicted_key in action_map:
            action_map[predicted_key]()
        else:
            print("Ação inválida prevista:", predicted_key)

        # Se estiver em modo de gravação, guarda os dados
        if self.record:
            with open("data/dataset.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.sensors + [predicted_key])

    def draw_sensors(self, win):
        center_x = self.x + self.img.get_width() // 2
        center_y = self.y + self.img.get_height() // 2

        for radar_angle in RADAR_ANGLES:
            angle = math.radians(self.angle + radar_angle + 90)
            dist = 0
            end_x, end_y = center_x, center_y

            for d in range(0, MAX_RADAR_DISTANCE, 2):
                dx = int(center_x + math.cos(angle) * d)
                dy = int(center_y - math.sin(angle) * d)

                if 0 <= dx < WIDTH and 0 <= dy < HEIGHT:
                    if TRACK_BORDER_MASK.get_at((dx, dy)) != 0:
                        break
                else:
                    break
                dist = d
                end_x, end_y = dx, dy

            pygame.draw.line(win, (255, 0, 0), (center_x, center_y), (end_x, end_y), 2)

            if 0 <= end_x < WIDTH and 0 <= end_y < HEIGHT:
                is_off_track = TRACK_MASK.get_at((end_x, end_y)) == 0
            else:
                is_off_track = True

            color = (255, 0, 0) if is_off_track else (0, 255, 0)
            pygame.draw.circle(win, color, (end_x, end_y), 4)

    def draw(self, win):
        super().draw(win)

    def next_level(self, level):
        from main import set_random_spawn
        set_random_spawn(self)
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02

    def rotLeft(self):
        self.rotate(left=True)

    def rotRight(self):
        self.rotate(right=True)

    def accelerate(self):
        self.move_forward()

    def brake(self):
        self.move_backwards()
