import pygame
from utils.path import PATH  # Usado para debug opcional do caminho da pista

# Escala uma imagem pelo fator fornecido
def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

# Roda uma imagem em torno do centro da sua posição original
def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

# Mostra texto centrado no ecrã
def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(
        render,
        (win.get_width() / 2 - render.get_width() / 2,
         win.get_height() / 2 - render.get_height() / 2)
    )

# Função principal para desenhar todos os elementos do jogo
def draw(win, images, player_car, computer_car, game_info,
         finish_image=None, finish_pos=None, finish_angle=0):
    
    # Desenha o fundo e camadas estáticas
    for img, pos in images:
        win.blit(img, pos)

    # Desenha a meta, se fornecida (posição, imagem, rotação)
    if finish_image and finish_pos is not None:
        blit_rotate_center(win, finish_image, finish_pos, finish_angle)

    # (Debug opcional) Mostra os pontos do PATH da pista
    # for point in PATH:
    #     pygame.draw.circle(win, (255, 0, 0), point, 5)

    # Informações de jogo (nível, tempo, velocidade)
    font = pygame.font.SysFont("comicsans", 44)
    level_text = game_info.level
    time_text = game_info.get_level_time()

    if player_car:
        vel_text = round(player_car.vel, 1)
    elif computer_car:
        vel_text = round(computer_car.vel, 1)
    else:
        vel_text = 0

    win.blit(font.render(f'Level {level_text}', 1, (255, 255, 255)), (10, win.get_height() - 130))
    win.blit(font.render(f'Time {time_text}', 1, (255, 255, 255)), (10, win.get_height() - 90))
    win.blit(font.render(f'Vel {vel_text} px/s', 1, (255, 255, 255)), (10, win.get_height() - 50))

    # Desenha os carros
    if player_car:
        player_car.draw(win)
    if computer_car:
        computer_car.draw(win)

    # Atualiza o ecrã
    pygame.display.update()
