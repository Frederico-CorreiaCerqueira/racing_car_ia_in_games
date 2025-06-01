import pygame
from utils.settings import TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION, WIN, MAIN_FONT
from utils.draw_helpers import blit_text_center

def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.bounce()

    if computer_car.collide(TRACK_BORDER_MASK, 0, 0):
                computer_car.bounce()

    if computer_car and computer_car.collide(FINISH_MASK, *FINISH_POSITION) is not None:
        blit_text_center(WIN, MAIN_FONT, "YOU LOST!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.next_level(1)
        return True
    

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


