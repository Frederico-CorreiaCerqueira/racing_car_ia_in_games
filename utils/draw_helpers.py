import pygame
from utils.path import PATH  # certificar-se de importar o PATH se ainda não estiver

# Escala uma imagem pelo fator dado
def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

# Roda a imagem mantendo o centro alinhado
def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

# Escreve texto centrado na janela
def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width()/2,
                      win.get_height()/2 - render.get_height()/2))

# Desenha o fundo, carros, textos de info
def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    # Para visualizar o PATH da pista (opcional)
    #for point in PATH:
    #    pygame.draw.circle(win, (255, 0, 0), point, 5)  # pontos vermelhos

    level_text = game_info.level
    time_text = game_info.get_level_time()

    # Usa a velocidade do player se existir, senão a do computador
    if player_car:
        vel_text = round(player_car.vel, 1)
    elif computer_car:
        vel_text = round(computer_car.vel, 1)
    else:
        vel_text = 0

    font = pygame.font.SysFont("comicsans", 44)
    win.blit(font.render(f'Level {level_text}', 1, (255, 255, 255)), (10, win.get_height()-130))
    win.blit(font.render(f'Time {time_text}', 1, (255, 255, 255)), (10, win.get_height()-90))
    win.blit(font.render(f'Vel {vel_text} px/s', 1, (255, 255, 255)), (10, win.get_height()-50))

    # Desenha os carros, se existirem
    if player_car:
        player_car.draw(win)
    if computer_car:
        computer_car.draw(win)

    pygame.display.update()
