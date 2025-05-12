import pygame

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def blit_text_center(win, font, text):
    render = font.render(text, 1, (255, 255, 255))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))

def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = game_info.level
    time_text = game_info.get_level_time()
    vel_text = round(player_car.vel, 1)

    font = pygame.font.SysFont("comicsans", 44)
    win.blit(font.render(f'Level {level_text}', 1, (255, 255, 255)), (10, win.get_height()-130))
    win.blit(font.render(f'Time {time_text}', 1, (255, 255, 255)), (10, win.get_height()-90))
    win.blit(font.render(f'Vel {vel_text} px/s', 1, (255, 255, 255)), (10, win.get_height()-50))

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width() /
                      2, win.get_height()/2 - render.get_height()/2))
