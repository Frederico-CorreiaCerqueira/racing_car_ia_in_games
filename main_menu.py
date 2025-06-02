import pygame
import sys
from main import run_game_manual, run_game_ai, run_game_from_middle

pygame.init()

WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu - IA Racing Game")
FONT = pygame.font.SysFont("comicsans", 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

options = [
    "1 - Play and Train",
    "2 - See AI Car (trains too)",
    "3 - Play from the middle"
]

def draw_menu(selected):
    WIN.fill(WHITE)
    title = FONT.render("Escolhe uma opção:", True, BLACK)
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 40))

    for i, text in enumerate(options):
        color = BLACK if i != selected else (0, 128, 255)
        option_surface = FONT.render(text, True, color)
        WIN.blit(option_surface, (60, 100 + i*60))

    pygame.display.update()

def main_menu():
    selected = 0
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        draw_menu(selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        run_game_manual()
                    elif selected == 1:
                        run_game_ai()
                    elif selected == 2:
                        run_game_from_middle()

if __name__ == "__main__":
    main_menu()
