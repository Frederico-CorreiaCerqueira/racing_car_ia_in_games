
import math

import numpy
import pygame

from decision_tree.decision_tree import Action,Boolean
from .abstract_car import AbstractCar
from settings import CAR_SIZE, GREEN_CAR, HEIGHT, RED, TRACK_MASK, WIDTH, YELLOW



acc=Action("accelerate")
rl=Action('rotLeft')
rr=Action('rotRight')
br=Action('brake')
right = Boolean("east?",rl, acc)
left = Boolean("west?",rr,right)
rightb = Boolean("east?",rl, br)
leftb = Boolean("west?",rr,rightb)
north = Boolean("north?",leftb,left)
decisionTreeSimple=north

class DTSimpleCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)
    SENSOR_POS = [(0, -50), (-20, -30), (20, -30), (0, 40)]
    SENSOR_NAMES = ['north',"west","east","south"]
    DT = decisionTreeSimple

    
    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        self.update_sensors()
        #self.sensors [WHITE, WHITE, WHITE, WHITE]
        # deveria ser feito o UPDATE_SENSORS para termos os primeiros valores
    
    def step(self):
        self.update_sensors()
        valores=dict()
        for i in range(4):  # oiderua ser len(self.sensors) rm vez de 4
            valores[self.SENSOR_NAMES[i]+"?"]=self.sensors[i][1] in (RED, YELLOW)
        # aqui teremos que devolver o dicionário com os nomes
        action=(self.DT).decide(valores)
        #print(valores,'------------------------->',action)
        eval('self.'+action+'()')
        
            
    def next_level(self,level):
        self.reset()
        self.vel=self.max_vel+(level-1)*0.02

        
    def draw_sensors(self, win):
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        dx, dy = CAR_SIZE[0], CAR_SIZE[1]
        alfa = math.radians(self.angle)
        mrot = numpy.array([[math.cos(alfa), -math.sin(alfa)], [math.sin(alfa), math.cos(alfa)]])
        pts = numpy.array(self.SENSOR_POS)
        npts = numpy.dot(pts, mrot)
        for i in npts:
            if 0<=i[0]+x<WIDTH and 0<=i[1]+y<HEIGHT: 
                pygame.draw.circle(win, TRACK_MASK.get_at((int(i[0] + x), int(i[1] + y))), \
                                                          (int(i[0] + x), int(i[1] + y)),2, 2)

    def draww_sensors(self, win):
        for (pos,color) in self.sensors:
            if color:
                pygame.draw.circle(win, color,pos,2, 2)
                
    def draw(self,win):
        super().draw(win)
        self.draw_sensors(win)
        

    def update_sensors(self):
        x, y = int(self.x + CAR_SIZE[0]), int(self.y + CAR_SIZE[1])
        dx, dy = CAR_SIZE[0], CAR_SIZE[1]
        alfa = self.angle * math.pi / 180
        mrot = numpy.array([[math.cos(alfa), -math.sin(alfa)], [math.sin(alfa), math.cos(alfa)]])
        pts = numpy.array(self.SENSOR_POS)
        npts = numpy.dot(pts, mrot)
        self.sensors = []
        for dx,dy in npts:
            color = TRACK_MASK.get_at((int(dx + x), int(dy + y))) if 0<=dx+x<WIDTH and 0<=dy+y<HEIGHT  else None
            self.sensors.append(((dx+x,dy+y),color))
            
     # Atomic Actions
    def rotLeft(self):
        self.rotate(True, False)


    def rotRight(self):
        self.rotate(False, True)


    def accelerate(self):
        """ control car acceleration according to its status """
        self.move_forward()


    def brake(self):
        """ control car acceleration according to its status """
        self.move_backwards()

