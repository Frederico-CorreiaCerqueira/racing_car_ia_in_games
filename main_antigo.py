import pygame
import sys
import random

from cars.dt_trained_car import DecisionTreeTrainedCar
from cars.player_car import PlayerCar
from utils.settings import *
from game.game_info import GameInfo
from game.collision import handle_collision
from utils.draw_helpers import draw, blit_text_center


def set_random_spawn(car):
    spawn_points = [
        ((57, 251), 180),     
        ((399, 600), 0),      
        ((730, 383), 30),     
        ((280, 93), 150)      
    ]
    pos, angle = random.choice(spawn_points)
    car.START_POS = pos
    car.x, car.y = pos
    car.angle = angle
    car.start_angle = angle  


def game_loop(player_car, computer_car):
    global WIN, WIDTH, HEIGHT

    pygame.init()
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("IA Racing Game")

    game_info = GameInfo()
    run = True
    clock = pygame.time.Clock()

 
    if player_car:
        player_car.reset()
    if computer_car:
        computer_car.reset()

    try:
        while run:
            clock.tick(FPS)
            draw(WIN, images, player_car, computer_car, game_info)

            while not game_info.started:
                blit_text_center(WIN, MAIN_FONT, f'Press any key to start level {game_info.level}!')
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return  
                        game_info.start_level()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  

    
            if player_car:
                player_car.move_player()
            if computer_car:
                computer_car.step()

  
            if handle_collision(player_car, computer_car, game_info):
                draw(WIN, images, player_car, computer_car, game_info)

            if game_info.game_finished():
                blit_text_center(WIN, MAIN_FONT, "YOU WON!")
                pygame.time.wait(5000)
                game_info.reset()
                if player_car:
                    player_car.reset()
                if computer_car:
                    set_random_spawn(computer_car)
                    computer_car.reset()
                    computer_car.next_level(1)

        pygame.quit()

    except Exception as e:
        print("Erro fatal:", e)
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


def run_game_manual():
    player_car = PlayerCar(4, 4)
    computer_car = DecisionTreeTrainedCar(4, 4, record=False)

    player_car.START_POS = (150, 200)
    player_car.x, player_car.y = (180, 200)
    player_car.angle = 0
    #player_car.start_angle = 0

    computer_car.START_POS = (180, 200)
    computer_car.x, computer_car.y = (150, 200)
    computer_car.angle = 0
    #computer_car.start_angle = 0

    game_loop(player_car, computer_car)



def run_game_ai():
    player_car = None
    computer_car = DecisionTreeTrainedCar(4, 4, record=False)


    set_random_spawn(computer_car)
    game_loop(player_car, computer_car)


def run_game_from_middle():
    player_car = PlayerCar(4, 4)
    computer_car = None
    set_random_spawn(player_car)
    game_loop(player_car, computer_car)


if __name__ == "__main__":
    run_game_manual()
