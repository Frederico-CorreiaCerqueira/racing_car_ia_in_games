import pygame
import sys
from cars.dt_simple_car import DTSimpleCar
from cars.dt_trained_car import DecisionTreeTrainedCar
from settings import *
from cars.player_car import PlayerCar
from cars.computer_car import ComputerCar
from game.game_info import GameInfo
from game.collision import handle_collision, move_player

from utils.draw_helpers import draw, blit_text_center


def main():
    player_car = PlayerCar(4, 4)
    #computer_car = DecisionTreeTrainedCar(4, 4)
    computer_car = DTSimpleCar(4, 4)
    game_info = GameInfo()
    run = True
    clock = pygame.time.Clock()

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

        move_player(player_car)
        computer_car.step()

        if handle_collision(player_car, computer_car, game_info):
            draw(WIN, images, player_car, computer_car, game_info)

        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "YOU WON!")
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car.next_level(1)

    pygame.quit()

if __name__ == "__main__":
    main()
