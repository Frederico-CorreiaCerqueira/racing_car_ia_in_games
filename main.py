import pygame
import sys
import pickle

from cars.computer_car import ComputerCar
from cars.dt_simple_car import DTSimpleCar
from cars.dt_trained_car import DecisionTreeTrainedCar
from cars.player_car import PlayerCar
from utils.settings import *
from game.game_info import GameInfo
from game.collision import handle_collision
from utils.draw_helpers import draw, blit_text_center

level_data_start_index = 0

def count_dataset_rows():
    try:
        with open("data/dataset.csv", "r") as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0

#def delete_last_level_data():
#    global level_data_start_index
#    try:
#        with open("data/dataset.csv", "r") as f:
#            lines = f.readlines()
#        with open("data/dataset.csv", "w") as f:
#            f.writelines(lines[:level_data_start_index])
#    except Exception as e:
#        print("Erro ao apagar dados:", e)

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
                        game_info.start_level()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

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
    computer_car = None
    game_loop(player_car, computer_car)

def run_game_ai():
    player_car = None
    computer_car = DecisionTreeTrainedCar(4, 4, record=True)
    game_loop(player_car, computer_car)

def run_game_from_middle():
    player_car = PlayerCar(4, 4)
    computer_car = None
    player_car.START_POS = (399,600)
    game_loop(player_car, computer_car)


if __name__ == "__main__":
    run_game_manual()
