import sys

import pygame
from pygame import *
import os

MOVE_SPEED = 1
WIDTH = 300
HEIGHT = 100
COLOR = "#888888"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


def load_image(name, colorkey=None):
    fullname = os.path.join(("%s/../../data/animations/Bar/" % __file__), name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    LI_image = pygame.image.load(fullname)
    if colorkey is not None:
        LI_image = LI_image.convert()
        if colorkey == -1:
            colorkey = LI_image.get_at((0, 0))
        LI_image.set_colorkey(colorkey)
    else:
        LI_image = LI_image.convert_alpha()
    return LI_image


class health_bar(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        self.max_hero_hp = 150
        self.now_hero_hp = 150

    def update(self, now_hp, max_hp, camera_x):
        self.image.fill(Color(COLOR))
        number_hp = int((now_hp / max_hp * 100) / 1.847)
        base_x_h_point = 80
        for i in range(number_hp):  # max_hp = 54
            self.image.blit(pygame.transform.scale(load_image("health_point.png"), (4, 20)), (base_x_h_point, 30))
            base_x_h_point += 4
        self.image.blit(pygame.transform.scale(load_image("health_bar.png"), (300, 75)), (0, 0))
        self.rect.x = abs(camera_x) + 40
