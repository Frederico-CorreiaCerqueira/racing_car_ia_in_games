import pygame
from settings import TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION, WIN, MAIN_FONT
from utils.draw_helpers import blit_text_center

def handle_collision(player_car, computer_car, game_info):
    if computer_car and computer_car.collide(FINISH_MASK, *FINISH_POSITION) is not None:
        if computer_car.vel < 0:
            computer_car.bounce()
        else:
            blit_text_center(WIN, MAIN_FONT, "YOU LOST!")
            pygame.display.update()
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car.next_level(1)
            return True



    # Colisão do jogador com linha de meta (ganha ou avança)
    poi = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if poi is not None:
        if poi[1] == 0:
            player_car.bounce()
        else:
            if game_info.level == game_info.LEVELS:
                blit_text_center(WIN, MAIN_FONT, "YOU WON!")
                pygame.display.update()
                pygame.time.wait(5000)
                game_info.reset()
                player_car.reset()
                if computer_car:
                    computer_car.next_level(1)
            else:
                player_car.reset()
                game_info.next_level()
                if computer_car:
                    computer_car.next_level(game_info.level)
            return True

    return False


def move_player(player_car):
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
