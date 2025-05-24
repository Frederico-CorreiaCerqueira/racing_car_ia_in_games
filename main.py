import pygame
import sys
import pickle
import random
import csv
import os

from cars.dt_simple_car import DTSimpleCar
from cars.dt_trained_car import DecisionTreeTrainedCar
from cars.player_car import PlayerCar
from settings import *
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

def delete_last_level_data():
    global level_data_start_index
    try:
        with open("data/dataset.csv", "r") as f:
            lines = f.readlines()
        with open("data/dataset.csv", "w") as f:
            f.writelines(lines[:level_data_start_index])
       # print("Dados do nível atual removidos com sucesso.")
    except Exception as e:
        print("Erro ao apagar dados:", e)

def main():
    pygame.init()

    player_car = PlayerCar(4, 4)
    computer_car = DecisionTreeTrainedCar(4, 4)

    game_info = GameInfo()
    run = True
    clock = pygame.time.Clock()

    player_trajectory = []
    ai_trajectory = []

    player_car.reset()
    computer_car.reset()

    player_start_pos = (player_car.x, player_car.y)
    computer_start_pos = (computer_car.x, computer_car.y)
    player_car.x, player_car.y = computer_start_pos
    computer_car.x, computer_car.y = player_start_pos

    reverse_race = random.choice([True, False])
    if reverse_race:
        player_car.angle += 45
        computer_car.angle += 45

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
                            global level_data_start_index
                            level_data_start_index = count_dataset_rows()
                            game_info.start_level()
                        elif event.key == pygame.K_r:
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
                        game_info.reset()
                        player_car.reset()
                        if computer_car:
                            computer_car.reset()
                    if event.key == pygame.K_k:
                        #print("Nível ignorado com tecla K")
                        player_car.reset()
                        if computer_car:
                            computer_car.reset()
                        delete_last_level_data()
                        game_info.next_level()
                        if computer_car:
                            computer_car.next_level(game_info.level)

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

            # Adiciona bounce se colidir com borda da pista
            if player_car.collide(TRACK_BORDER_MASK, 0, 0):
                player_car.bounce()

            if computer_car and computer_car.collide(TRACK_BORDER_MASK, 0, 0):
                computer_car.bounce()

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
