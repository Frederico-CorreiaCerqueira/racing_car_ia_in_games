import pygame
import sys
import random
import math

from cars.computer_car import ComputerCar
from cars.dt_simple_car import DTSimpleCar
from cars.dt_trained_car import DecisionTreeTrainedCar
from cars.player_car import PlayerCar
from utils.settings import *
from game.game_info import GameInfo
from game.collision import handle_collision
from utils.draw_helpers import draw, blit_text_center

def set_random_spawn(car):
    spawn_points = [
        ((590, 620), 180),
        ((57, 251), 180),
        ((399, 600), 0),
        ((180, 200), 0),
    ]
    pos, angle = random.choice(spawn_points)
    car.START_POS = pos
    car.x, car.y = pos
    car.angle = angle
    car.start_angle = angle

def place_finish_behind(car, distance=60):
    global FINISH_POSITION, FINISH_ANGLE, FINISH_MASK, images

    angle_deg = car.angle
    angle_rad = math.radians(angle_deg - 90)

    center_x = car.x + car.img.get_width() / 2
    center_y = car.y + car.img.get_height() / 2

    dx = -math.cos(angle_rad) * distance
    dy = -math.sin(angle_rad) * distance
    meta_center_x = center_x + dx
    meta_center_y = center_y + dy

    rotated_finish = pygame.transform.rotate(FINISH, angle_deg)
    rotated_rect = rotated_finish.get_rect(center=(meta_center_x, meta_center_y))
    FINISH_POSITION = (rotated_rect.x, rotated_rect.y)

    FINISH_ANGLE = angle_deg
    FINISH_MASK = pygame.mask.from_surface(rotated_finish)

    images = [
        (GRASS, (0, 0)),
        (TRACK, (0, 0)),
        (TRACK_BORDER, (0, 0))
    ]

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

            draw(WIN, images, player_car, computer_car, game_info,
                 finish_image=FINISH, finish_pos=FINISH_POSITION, finish_angle=FINISH_ANGLE)

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

            # Verifica colisões e atualiza se necessário
            if handle_collision(
                player_car,
                computer_car,
                game_info,
                FINISH_MASK,
                FINISH_POSITION,
                set_spawn_fn=set_random_spawn,
                place_finish_fn=place_finish_behind
            ):
                draw(WIN, images, player_car, computer_car, game_info,
                     finish_image=FINISH, finish_pos=FINISH_POSITION, finish_angle=FINISH_ANGLE)

            # Reset total quando termina o jogo
            if game_info.game_finished():
                blit_text_center(WIN, MAIN_FONT, "YOU WON!")
                pygame.display.update()
                pygame.time.wait(5000)
                game_info.reset()

                if player_car and not computer_car:
                    set_random_spawn(player_car)
                    place_finish_behind(player_car)
                    player_car.reset()

                elif computer_car and not player_car:
                    set_random_spawn(computer_car)
                    place_finish_behind(computer_car)
                    computer_car.reset()
                    computer_car.next_level(1)

                elif player_car and computer_car:
                    set_random_spawn(player_car)
                    place_finish_behind(player_car)
                    player_car.reset()
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
    player_car.x, player_car.y = (150, 200)
    player_car.angle = 0

    computer_car.START_POS = (180, 200)
    computer_car.x, computer_car.y = (180, 200)
    computer_car.angle = 0

    place_finish_behind(player_car)

    game_loop(player_car, computer_car)


def run_game_ai():
    player_car = None
    computer_car = DecisionTreeTrainedCar(4, 4, record=False)

    set_random_spawn(computer_car)
    place_finish_behind(computer_car)
    game_loop(player_car, computer_car)

def run_game_from_middle():
    player_car = PlayerCar(4, 4)
    computer_car = None

    set_random_spawn(player_car)
    place_finish_behind(player_car)
    game_loop(player_car, computer_car)

if __name__ == "__main__":
     run_game_manual()
    #run_game_ai()
    # run_game_from_middle()
