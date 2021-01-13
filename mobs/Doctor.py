import sys

import pygame
from pygame import *
from hero import playanim as pyganim
import os
from random import randint

MOVE_SPEED = 1
WIDTH = 51
HEIGHT = 48
COLOR = "#888888"
GRAVITY = 0.35
ANIMATION_DELAY = 0.1  # скорость смены кадров
ANIMATION_DELAY_ATTACK = 0.1  # скорость смены кадров
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

RUN_RIGHT = [
    ('%s/../data/animations/doctor/movement_right/1.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_right/2.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_right/3.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_right/4.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_right/5.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_right/6.png' % ICON_DIR)
]

RUN_LEFT = [
    ('%s/../data/animations/doctor/movement_left/1.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_left/2.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_left/3.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_left/4.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_left/5.png' % ICON_DIR),
    ('%s/../data/animations/doctor/movement_left/6.png' % ICON_DIR)
]

IDLE_RIGHT = [
    ('%s/../data/animations/doctor/idle_right/1.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_right/2.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_right/3.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_right/4.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_right/5.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_right/6.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_right/7.png' % ICON_DIR)
]

IDLE_LEFT = [
    ('%s/../data/animations/doctor/idle_left/1.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_left/2.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_left/3.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_left/4.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_left/5.png' % ICON_DIR),
    ('%s/../data/animations/doctor/idle_left/6.png' % ICON_DIR)
]

HIT_RIGHT = [
    ('%s/../data/animations/doctor/hit_right/1.png' % ICON_DIR),
    ('%s/../data/animations/doctor/hit_right/2.png' % ICON_DIR),
    ('%s/../data/animations/doctor/hit_right/3.png' % ICON_DIR)
]

HIT_LEFT = [
    ('%s/../data/animations/doctor/hit_left/1.png' % ICON_DIR),
    ('%s/../data/animations/doctor/hit_left/2.png' % ICON_DIR),
    ('%s/../data/animations/doctor/hit_left/3.png' % ICON_DIR)
]

ATTACK_LEFT = [
    ('%s/../data/animations/doctor/attack_left/1.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_left/2.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_left/3.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_left/4.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_left/5.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_left/6.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_left/7.png' % ICON_DIR)
]

ATTACK_RIGHT = [
    ('%s/../data/animations/doctor/attack_right/1.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_right/2.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_right/3.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_right/4.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_right/5.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_right/6.png' % ICON_DIR),
    ('%s/../data/animations/doctor/attack_right/7.png' % ICON_DIR)
]


def load_image(name, colorkey=None):
    fullname = os.path.join(("%s/../../data/assets/mob_bar/" % __file__), name)
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


class Doctor(sprite.Sprite):
    def __init__(self, x, y):
        # ____________________-DEMONS FEATURES-___________________________

        self.health_points = 200
        self.max_hp = self.health_points
        self.damage = 70

        # ____________________-DEMONS FEATURES-___________________________

        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения

        self.POSITION_RIGHT = False
        self.onGround = False  # На земле ли я?
        self.total_damage = 0

        self.image = Surface((WIDTH + 10, HEIGHT + 40))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT + 30)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным

        self.image_hp = Surface((40, 10))
        self.image_hp.fill(Color(COLOR))
        self.image_hp.set_colorkey(Color(COLOR))  # делаем фон прозрачным

        # Анимация движения вправо
        boltAnim = []
        for anim in RUN_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltRunRight = pyganim.PygAnimation(boltAnim)
        self.boltRunRight.play()

        boltAnim = []
        for anim in RUN_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltRunLeft = pyganim.PygAnimation(boltAnim)
        self.boltRunLeft.play()

        boltAnim = []
        for anim in IDLE_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltIdleRight = pyganim.PygAnimation(boltAnim)
        self.boltIdleRight.play()

        boltAnim = []
        for anim in IDLE_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltIdleLeft = pyganim.PygAnimation(boltAnim)
        self.boltIdleLeft.play()

        boltAnim = []
        for anim in HIT_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltHitLeft = pyganim.PygAnimation(boltAnim)
        self.boltHitLeft.play()

        boltAnim = []
        for anim in HIT_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltHitRight = pyganim.PygAnimation(boltAnim)
        self.boltHitRight.play()

        boltAnim = []
        for anim in ATTACK_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY_ATTACK))
        self.boltAttackLeft = pyganim.PygAnimation(boltAnim, loop=False)

        boltAnim = []
        for anim in ATTACK_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY_ATTACK))
        self.boltAttackRight = pyganim.PygAnimation(boltAnim, loop=False)

        self.attack_time = self.boltAttackLeft.startTimes[-1]  # Брать из метода _startTimes текущей анимаци
        self.attack_flag = False

    def doctor_behavior(self, hero_x, hero_y, platforms):
        # ____________________________________________________________________________________________________________________

        if -75 <= int(hero_y) - 15 - self.rect.y <= 75 and 0 <= int(hero_x) - int(self.rect.x) <= 40 \
                and self.POSITION_RIGHT:
            self.xvel = 0
            self.image.fill(Color(COLOR))
            self.POSITION_RIGHT = True
            self.boltAttackRight.blit(self.image, (0, 0))
            self.boltAttackRight.play()

            if self.boltAttackRight.elapsed >= self.attack_time - 0.1 and not self.attack_flag:
                self.boltAttackRight.stop()
                self.attack_flag = True
                self.total_damage += randint(self.damage - 6, self.damage + 2)

        # ____________________________________________________________________________________________________________________

        elif -75 <= int(hero_y) - 15 - self.rect.y <= 75 and 0 <= int(self.rect.x) - int(hero_x) <= 10 \
                and not self.POSITION_RIGHT:
            self.xvel = 0
            self.POSITION_RIGHT = False
            self.image.fill(Color(COLOR))
            self.boltAttackLeft.blit(self.image, (0, 0))
            self.boltAttackLeft.play()

            if self.boltAttackLeft.elapsed >= self.attack_time - 0.1 and not self.attack_flag:
                self.boltAttackLeft.stop()
                self.attack_flag = True
                self.total_damage += randint(self.damage - 6, self.damage + 2)

        # ____________________________________________________________________________________________________________________

        elif -75 <= int(hero_y) - 15 - self.rect.y <= 75 and 0 <= int(self.rect.x) - int(hero_x) <= 350:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            self.POSITION_RIGHT = False
            self.boltRunLeft.blit(self.image, (0, 0))

        elif -75 <= int(hero_y) - 15 - self.rect.y <= 75 and 0 <= abs(int(hero_x) - int(self.rect.x)) <= 350:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            self.POSITION_RIGHT = True
            self.boltRunRight.blit(self.image, (0, 0))

        elif self.POSITION_RIGHT:
            self.xvel = 0
            self.image.fill(Color(COLOR))
            self.boltIdleRight.blit(self.image, (0, 0))

        elif not self.POSITION_RIGHT:
            self.xvel = 0
            self.image.fill(Color(COLOR))
            self.boltIdleLeft.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        if self.max_hp != self.health_points:
            self.image_hp.fill(Color(COLOR))
            #self.image_hp.blit(pygame.transform.scale(load_image("bar.png"), (30, 11)), (0, 0))
            base_x = 0
            num_hp = int(self.health_points / self.max_hp * 100 / 6.25)
            print(num_hp)
            for i in range(num_hp):
                self.image_hp.blit(pygame.transform.scale(load_image("bar_part_2.png"), (2, 7)), (base_x, 0))
                base_x += 2
            if self.POSITION_RIGHT:
                self.image.blit(self.image_hp, (5, 70))
            else:
                self.image.blit(self.image_hp, (30, 70))

        if self.health_points <= 0:
            self.rect.y = 3000

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

    def get_tick_damage(self):
        value = self.total_damage
        self.total_damage = 0
        self.attack_flag = False
        return value

    def dam_hero(self, value, x_hero, delta):
        if value is not None:
            if delta > 0:
                if x_hero <= self.rect.x <= x_hero + delta:
                    self.health_points -= value
                    print(value)
            if delta < 0:
                if x_hero + delta <= self.rect.x <= x_hero:
                    self.health_points -= value
                    print(value)
