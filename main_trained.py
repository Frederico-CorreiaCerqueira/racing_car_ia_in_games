import pygame
import sys
import pickle

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
    game_info = GameInfo()
    run = True
    clock = pygame.time.Clock()

    player_trajectory = []
    ai_trajectory = []

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

            # Grava trajetórias (apenas um extra)
            player_trajectory.append((player_car.x, player_car.y))
            ai_trajectory.append((computer_car.x, computer_car.y))

            # Verifica colisões
            if handle_collision(player_car, computer_car, game_info):
                draw(WIN, images, player_car, computer_car, game_info)

            # Fim do jogo
            if game_info.game_finished():
                blit_text_center(WIN, MAIN_FONT, "YOU WON!")
                pygame.time.wait(5000)
                game_info.reset()
                player_car.reset()
                computer_car.next_level(1)

        pygame.quit()

    finally:
        # Grava as trajetórias em ficheiro
        with open("trajectories.pkl", "wb") as f:
            pickle.dump({
                "player": player_trajectory,
                "ai": ai_trajectory
            }, f)

        print("Trajetórias guardadas em trajectories.pkl")
        sys.exit()


if __name__ == "__main__":
    main()
