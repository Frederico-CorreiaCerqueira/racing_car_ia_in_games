import pygame
from utils.settings import TRACK_BORDER_MASK, WIN, MAIN_FONT
from utils.draw_helpers import blit_text_center

# Função para verificar colisões do(s) carro(s)
def handle_collision(player_car, computer_car, game_info, finish_mask, finish_pos,
                     set_spawn_fn=None, place_finish_fn=None):
    # Colisão com a borda
    if player_car and player_car.collide(TRACK_BORDER_MASK) is not None:
        player_car.bounce()

    # Colisão do computador com a meta (vitória da IA)
    if computer_car and computer_car.collide(finish_mask, *finish_pos) is not None:
        blit_text_center(WIN, MAIN_FONT, "YOU LOST!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()

        # Reposiciona ambos os carros e a meta
        if set_spawn_fn and place_finish_fn:
            if computer_car:
                set_spawn_fn(computer_car)
                place_finish_fn(computer_car)
            if player_car:
                set_spawn_fn(player_car)
                place_finish_fn(player_car)

        if player_car:
            player_car.reset()
        if computer_car:
            computer_car.reset()
            computer_car.next_level(1)
        return True

    # Colisão do jogador com a meta
    if player_car:
        poi = player_car.collide(finish_mask, *finish_pos)
        if poi is not None:
            if poi[1] == 0:
                player_car.bounce()
            else:
                if set_spawn_fn and place_finish_fn:
                    set_spawn_fn(player_car)
                    place_finish_fn(player_car)

                if game_info.level == game_info.LEVELS:
                    blit_text_center(WIN, MAIN_FONT, "YOU WON!")
                    pygame.display.update()
                    pygame.time.wait(5000)
                    game_info.reset()
                    player_car.reset()
                    if computer_car:
                        computer_car.next_level(1)
                else:
                    game_info.next_level()
                    player_car.reset()
                    if computer_car:
                        computer_car.next_level(game_info.level)
                return True

    return False
