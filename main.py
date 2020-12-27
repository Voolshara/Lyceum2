# Импортируем библиотеку pygame
from pprint import pprint

import pygame
from pygame import *
from blocks import *
from hero import *

# Объявляем переменные
WIN_WIDTH = 1280  # Ширина создаваемого окна
WIN_HEIGHT = 720  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"
PLATFORM_WIDTH = 20
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = "#FFFFFF"
FPS = 60


def load_level(filename):
    filename = "data/maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы
    return Rect(l, t, w, h)


if __name__ == "__main__":
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Dungeon adventure")  # Пишем в шапку
    background = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    background.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    hero = Player(100, 30)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)

    clock = pygame.time.Clock()
    x = y = 0
    level = load_level("lvl1.txt")
    for row in level:  # вся строка
        for char in row:  # каждый символ
            if char == "#":
                # создаем блок, заливаем его цветом и рисеум его
                platform = Platform(x, y)
                entities.add(platform)
                platforms.append(platform)
            else:
                empty = Empty(x, y)
                entities.add(empty)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    running = True
    while running:  # Основной цикл программы
        clock.tick(FPS)
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_d:
                    right = True
                if event.key == K_a:
                    left = True
                if event.key == K_w:
                    up = True

            elif event.type == KEYUP:
                if event.key == K_d:
                    right = False
                if event.key == K_a:
                    left = False
                if event.key == K_w:
                    up = False

        screen.blit(background, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение
        for element in entities:
            screen.blit(element.image, camera.apply(element))
        screen.blit(hero.image, camera.apply(hero))
        pygame.display.update()  # обновление и вывод всех изменений на экран
        pygame.display.flip()
        print(clock.get_fps())
