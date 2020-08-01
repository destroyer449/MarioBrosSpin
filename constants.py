import sys
import os

import pygame
import pygame.event as py_event
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "images")


def load_image(name, colorkey=None):
    try:
        fullname = os.path.join(data_dir, name)
        image = pygame.image.load(fullname)
    except TypeError:
        raise pygame.error
    except pygame.error:
        print('Cannot load image:', fullname)
        raise pygame.error(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


# basic screen functions
def draw_text(surf, text, size, x=0, y=0, color=(255, 255, 255)):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def pause():
    ready = False
    draw_text(window, "PAUSED", 85, windowWidth // 2, 300)
    draw_text(window, "Press Space To Continue", 40, windowWidth // 2, 400)
    pygame.display.update()
    while not ready:
        for event in py_event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    ready = True
                if event.key == pygame.K_ESCAPE:
                    quit_game()
            if event.type == pygame.QUIT:
                quit_game()
        pygame.time.delay(1)


def quit_game():
    pygame.quit()
    sys.exit("quit")


resizable = input("resizable? [y/n]")
if resizable is True or resizable == "y" or resizable == "yes":
    windowWidth = 1080
    windowHeight = 750
    window = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
else:
    windowWidth = 850
    windowHeight = 850
    window = pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)
icon = pygame.image.load(os.path.join(data_dir, "mario.png"))
# icon.set_colorkey(icon.get_at((0, 0)), pygame.RLEACCEL)
pygame.display.set_icon(icon)
pygame.display.set_caption("PyGame")
font_name = pygame.font.match_font('times')
gravity = 0.015
rounds = 1
white = (255, 255, 255)
objects = pygame.sprite.RenderUpdates()
platforms = pygame.sprite.Group()
