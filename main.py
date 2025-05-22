import pygame
import sys
import pickle
import random

from cars.dt_simple_car import DTSimpleCar
from cars.dt_trained_car import DecisionTreeTrainedCar
from cars.player_car import PlayerCar
from settings import *
from game.game_info import GameInfo
from game.collision import handle_collision
from utils.draw_helpers import draw, blit_text_center


def main():
    pygame.init()

    player_car = PlayerCar(4, 4)
    computer_car = DecisionTreeTrainedCar(4, 4)
    # computer_car = DTSimpleCar(4, 4)

    game_info = GameInfo()
    run = True
    clock = pygame.time.Clock()

    player_trajectory = []
    ai_trajectory = []

    # Reset inicial com posição e ângulo aleatórios
    player_car.reset()
    computer_car.reset()

    # Troca de posições na linha de partida
    player_start_pos = (player_car.x, player_car.y)
    computer_start_pos = (computer_car.x, computer_car.y)
    player_car.x, player_car.y = computer_start_pos
    computer_car.x, computer_car.y = player_start_pos

    # Variação adicional: corrida invertida (anti-clockwise)
    reverse_race = random.choice([True, False])
    if reverse_race:
        player_car.angle += 180
        computer_car.angle += 180

    try:
        while run:
            clock.tick(FPS)
            draw(WIN, images, player_car, computer_car, game_info)

            while not game_info.started:
                blit_text_center(WIN, MAIN_FONT, f'Press SPACE to start level {game_info.level}!')
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game_info.start_level()
                        elif event.key == pygame.K_r:
                           # print("Restart")
                            game_info.reset()
                            player_car.reset()
                            if computer_car:
                                computer_car.reset()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                      #  print("Restart")
                        game_info.reset()
                        player_car.reset()
                        if computer_car:
                            computer_car.reset()

            # Controlos do jogador
            keys = pygame.key.get_pressed()
            moved = False
            if keys[pygame.K_a]:
                player_car.rotate(left=True)
                player_car.save_data("a")
            if keys[pygame.K_d]:
                player_car.rotate(right=True)
                player_car.save_data("d")
            if keys[pygame.K_w]:
                moved = True
                player_car.move_forward()
                player_car.save_data("w")
            if keys[pygame.K_s]:
                moved = True
                player_car.move_backwards()
                player_car.save_data("s")
            if not moved:
                player_car.reduce_speed()

            computer_car.step()

            # Grava trajetórias
            player_trajectory.append((player_car.x, player_car.y))
            ai_trajectory.append((computer_car.x, computer_car.y))

            if handle_collision(player_car, computer_car, game_info):
                draw(WIN, images, player_car, computer_car, game_info)

            if game_info.game_finished():
                blit_text_center(WIN, MAIN_FONT, "YOU WON!")
                pygame.time.wait(5000)
                game_info.reset()
                player_car.reset()
                computer_car.next_level(1)

        pygame.quit()

    finally:
        try:
            with open("trajectories.pkl", "wb") as f:
                pickle.dump({
                    "player": player_trajectory,
                    "ai": ai_trajectory
                }, f)
            print("Trajetórias guardadas em trajectories.pkl")
        except Exception as e:
            print("Erro ao guardar trajetórias:", e)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
