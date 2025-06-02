import pygame
from utils.settings import TRACK_BORDER_MASK, FINISH_MASK, FINISH_POSITION, WIN, MAIN_FONT
from utils.draw_helpers import blit_text_center

# Função para verificar colisões do(s) carro(s)
def handle_collision(player_car, computer_car, game_info):
    # Colisão do jogador com a borda
    if player_car and player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.bounce()

    # Colisão do computador com a linha de meta (perde)
    if computer_car and computer_car.collide(FINISH_MASK, *FINISH_POSITION) is not None:
        blit_text_center(WIN, MAIN_FONT, "YOU LOST!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        if player_car:
            player_car.reset()
        computer_car.next_level(1)
        return True

    # Colisão do jogador com a linha de meta
    if player_car:
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
