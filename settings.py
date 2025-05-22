import pygame
from utils.draw_helpers import scale_image
from path import PATH

# Load and scale images
GRASS = scale_image(pygame.image.load("assets/imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("assets/imgs/track.png"), 0.9)
TRACK_BORDER = scale_image(pygame.image.load("assets/imgs/track-border.png"), 0.9)
FINISH = pygame.image.load("assets/imgs/finish.png")
RED_CAR = scale_image(pygame.image.load("assets/imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("assets/imgs/green-car.png"), 0.55)

# Load and process the track mask
TRACK_MASK_SURFACE = scale_image(pygame.image.load("assets/imgs/track-mask.png"), 0.9)
TRACK_MASK = pygame.mask.from_surface(TRACK_MASK_SURFACE)

# Masks
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH_MASK = pygame.mask.from_surface(FINISH)

# Sizes
car_width, car_height = GREEN_CAR.get_size()
HALF_WIDTH, HALF_HEIGHT = car_width / 2, car_height / 2
CAR_SIZE = (HALF_WIDTH, HALF_HEIGHT)

# Screen setup
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

pygame.font.init()
MAIN_FONT = pygame.font.SysFont("comicsans", 44)
FPS = 60

# Colors
RED = (255, 0, 0, 255)
WHITE = (255, 255, 255, 255)
YELLOW = (255, 255, 0, 255)

# Images and positions
FINISH_POSITION = (130, 250)
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
