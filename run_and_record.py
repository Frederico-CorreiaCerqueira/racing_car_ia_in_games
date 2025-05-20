import pygame
import sys
import os
from cars.player_car import PlayerCar
from cars.sklearn_car import SklearnCar
from settings import *
from game.game_info import GameInfo
from game.collision import handle_collision, move_player
from utils.draw_helpers import draw, blit_text_center
from data.collect_data import save_data

def main():
    player_car = PlayerCar(4, 4)
    ai_car = SklearnCar(4, 4) if os.path.exists("classifier.joblib") else None
    game_info = GameInfo()
    run = True
    clock = pygame.time.Clock()

    player_trajectory = []
    ai_trajectory = []

    try:
        while run:
            clock.tick(FPS)
            draw(WIN, images, player_car, ai_car, game_info)

            while not game_info.started:
                blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        return
                    if event.type == pygame.KEYDOWN:
                        game_info.start_level()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    return

            keys = pygame.key.get_pressed()
            moved = False
            if keys[pygame.K_a]:
                player_car.rotate(left=True)
            if keys[pygame.K_d]:
                player_car.rotate(right=True)
            if keys[pygame.K_w]:
                moved = True
                player_car.move_forward()
            if keys[pygame.K_s]:
                moved = True
                player_car.move_backwards()
            if not moved:
                player_car.reduce_speed()

            if moved:
                sensor_vals = player_car.get_radar_distances()
                if keys[pygame.K_a]:
                    save_data(sensor_vals, "rotLeft")
                elif keys[pygame.K_d]:
                    save_data(sensor_vals, "rotRight")
                elif keys[pygame.K_s]:
                    save_data(sensor_vals, "brake")
                else:
                    save_data(sensor_vals, "accelerate")

            if ai_car:
                ai_car.step()
                ai_trajectory.append((ai_car.x, ai_car.y))

            player_trajectory.append((player_car.x, player_car.y))

            if handle_collision(player_car, ai_car, game_info):
                draw(WIN, images, player_car, ai_car, game_info)

            if game_info.game_finished():
                blit_text_center(WIN, MAIN_FONT, "YOU WON!")
                pygame.display.update()
                pygame.time.wait(5000)
                run = False  # sai do loop principal

    finally:
        pygame.quit()
        import pickle
        with open("trajectories.pkl", "wb") as f:
            pickle.dump({"player": player_trajectory, "ai": ai_trajectory}, f)
        print("Trajectories saved to trajectories.pkl")
        sys.exit()

if __name__ == "__main__":
    main()
