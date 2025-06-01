import math
import joblib
import pandas as pd

from .abstract_car import AbstractCar
from utils.settings import GREEN_CAR

SENSOR_NAMES = ['s1', 's2', 's3', 's4', 's5']


class DecisionTreeTrainedCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (180, 200)

    def __init__(self, max_vel, rotation_vel, model_path="model/classifier_with_initialPos_variation.joblib"):
        super().__init__(max_vel, rotation_vel)
        self.DT = joblib.load(model_path)
        self.sensors = []

        self.last_positions = []
        self.stuck_counter = 0
        
    def move(self):
        super().move()
      

    def step(self):
        self.sensors = self.get_radar_distances()
        df = pd.DataFrame([self.sensors], columns=SENSOR_NAMES)
        predicted_key = self.DT.predict(df)[0]

        print(f"Sensors: {self.sensors} → Action: {predicted_key}")

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


    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.02
        self.center_x = self.x + self.IMG.get_width() // 2
        self.center_y = self.y + self.IMG.get_height() // 2

    def rotLeft(self):
        self.rotate(left=True)

    def rotRight(self):
        self.rotate(right=True)

    def accelerate(self):
        self.move_forward()

    def brake(self):
        self.move_backwards()


    """def bounce(self):
        self.vel = -self.vel
        self.rotLeft()  
        #self.vel = 0"""
       


    def stuck(self):
        # 🚨 Verificar progresso:
        self.last_positions.append((self.x, self.y))
        #print(f"Posição atual: {self.x}, {self.y} → Últimas posições: {self.last_positions[-5:]}")
        if len(self.last_positions) > 10:
            self.last_positions.pop(0)

        ## Verificar se está “parado” (pouco movimento nos últimos 10 frames)
        if len(self.last_positions) == 10:
            total_movement = sum(
                math.hypot(self.last_positions[i][0] - self.last_positions[i-1][0],
                        self.last_positions[i][1] - self.last_positions[i-1][1])
                for i in range(1, 10)
            )
            if total_movement < 15:  
                self.stuck_counter += 1
                #print(f"Stuck counter: {self.stuck_counter}")
            else:
                self.stuck_counter = 0

            if self.stuck_counter > 30:  # 30 frames stuck? Corrige!
                print("🚨 O carro está preso! Fazendo correcção...")
                self.brake()
                self.rotLeft()  # ou rotLeft(), ou brake()
                self.accelerate()  # tenta sair do stuck
                return  # ignora a ação prevista e corrige