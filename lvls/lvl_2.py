import json

from mobs.Doctor import *
from lvls.blocks import *
from hero.hero import *
from hero.hero_hp import *
from fps_measurement import *
import option_menu as options
import mobs.Boss_code as Boss_code

# Объявляем переменные
WIN_WIDTH = 1280  # Ширина создаваемого окна
WIN_HEIGHT = 720  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"
PLATFORM_WIDTH = 20
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = "#FFFFFF"


def load_level(filename):
    filename = "data/maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join(("%s/../../data/assets/" % __file__), name)
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


def load_bg(name, colorkey=None):
    fullname = os.path.join(("%s/../../data/assets/" % __file__), name)
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


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move([self.state.topleft[0], self.state.topleft[1]])

    def apply_new(self, target):
        return target.move([self.state.topleft[0], self.state.topleft[1]])

    def update(self, target):
        self.state = self.camera_func(self.state, Rect(target.rect.x, target.rect.y, target.rect.w, target.rect.h))


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы
    return Rect(l, t, w, h)


def battle_music(_isLive=True):
    # __________________________________-DOWNLOAD OPTIONS-________________________________
    json_file_object_music = open("options.json", "r")
    json_dict_music = json.load(json_file_object_music)
    json_file_object_music.close()
    # __________________________________-DOWNLOAD OPTIONS-________________________________
    value = json_dict_music["music_value"] - int(json_dict_music["music_value"] / 2)
    if _isLive:
        if randint(1, 1) == 1:
            pygame.mixer.music.load('%s/../../data/music/battle.mp3' % __file__)
        pygame.mixer.music.set_volume(value)
        pygame.mixer.music.play(-1)
    else:
        print("LOL YOU DIE HAHAHAHHAHAHAHAHA")
        pygame.mixer.music.unload()
        pygame.mixer.music.load('%s/../../data/music/death.mp3' % __file__)
        pygame.mixer.music.play()


def save_game(x_hero, y_hero, hero_hp, json_dict):
    save_dict = dict()
    save_dict["x_hero"] = x_hero
    save_dict["y_hero"] = y_hero
    save_dict["hp_hero"] = hero_hp
    json_dict["last_lvl"] = 2
    json_dict["Save"] = save_dict
    with open('options.json', 'w') as outfile:
        json.dump(json_dict, outfile)


def DrawLvl(x_hero_input=150, y_hero_input=500, now_hero_hp=250):
    # __________________________________-DOWNLOAD OPTIONS-________________________________

    json_file_object = open("options.json", "r")
    json_dict = json.load(json_file_object)
    FPS = json_dict['FPS']

    # __________________________________-DOWNLOAD OPTIONS-________________________________

    pygame.init()  # Инициация PyGame, обязательная строчка

    _isAlive = True
    _is_music_pause = True
    battle_music(_isLive=_isAlive)
    save_flag = False
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Dungeon adventure")  # Пишем в шапку
    background = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    background.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    hero = Player(x_hero_input, y_hero_input, now_hero_hp)  # создаем героя по (x,y) координатам

    boss = Boss_code.Boss(200, 500)

    hero_hp = health_bar(50, 70)
    fps_label = fps_measure(1200, 70)

    left = right = False  # по умолчанию - стоим
    attack = up = ability = False
    global_pause = use_pause = green_label = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    clock = pygame.time.Clock()
    x = y = 0
    level = load_level("lvl2.txt")
    for row in level:  # вся строка
        for char in row:  # каждый символ
            if char == "p":
                platform = PlatformLvl1(x - 15, y)
                entities.add(platform)
                platforms.append(platform)
            if char == "e":
                earth = EarthLvl1(x - 15, y)
                entities.add(earth)
                platforms.append(earth)
            if char == "~":
                extra_earth = ExtraEarthLvl1(x - 15, y)
                entities.add(extra_earth)
                platforms.append(extra_earth)
            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    entities.add(boss)
    entities.add(hero_hp)
    entities.add(fps_label)

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    bg_castle = pygame.transform.scale(load_bg("background_images/bg_tree_2.png"), (1280, 720))

    camera = Camera(camera_configure, total_level_width, total_level_height)

    transparent_pause = pygame.Surface((1280, 720))
    transparent_pause.set_alpha(150)
    transparent_pause.fill((50, 50, 50))

    transparent_pause_all = pygame.Surface((1280, 720))
    transparent_pause_all.set_alpha(255)
    transparent_pause_all.fill((50, 50, 50))

    transparent_surface = pygame.Surface((1280, 720))
    transparent_surface.set_alpha(50)
    transparent_surface.fill((50, 50, 50))

    pause_menu = 1

    main_font = pygame.font.SysFont('Comic Sans MS', 130)
    label_font = pygame.font.SysFont('Comic Sans MS', 50)

    transparent_death = pygame.Surface((1280, 720))
    transparent_death.set_alpha(255)
    transparent_death.fill((0, 0, 0))

    back_font = pygame.font.SysFont('Comic Sans MS', 50)
    bacK_label = back_font.render('<<Back to menu', False, (153, 24, 24))

    pause_label = main_font.render('Pause', False, (255, 255, 255))

    running = True
    while running:  # Основной цикл программы
        clock.tick(FPS)
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT:
                running = False
                sys.exit()
            if not _isAlive:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        running = False
            elif event.type == KEYDOWN:
                if event.key == K_d:
                    right = True
                if event.key == K_a:
                    left = True
                if event.key == K_w:
                    up = True
                if event.key == K_i:
                    attack = True
                if event.key == K_p:
                    ability = True
                if event.key == K_ESCAPE:
                    if not global_pause:
                        global_pause = True
                    else:
                        global_pause = False
                        use_pause = False
                if global_pause:
                    if event.key == K_DOWN:
                        pause_menu += 1
                        if green_label:
                            green_label = False
                    if event.key == K_UP:
                        pause_menu -= 1
                        if green_label:
                            green_label = False
                    if event.key == K_RETURN:
                        if pause_menu == 1:
                            global_pause = False
                            use_pause = False
                        if pause_menu == 2:
                            save_flag = True
                        if pause_menu == 3:
                            options.launch_menu()
                            screen.blit(transparent_pause_all, (0, 0))
                            screen.blit(pause_label, (475, 50))
                        if pause_menu == 4:
                            running = False

            elif event.type == KEYUP:
                if event.key == K_d:
                    right = False
                if event.key == K_a:
                    left = False
                if event.key == K_w:
                    up = False
                if event.key == K_i:
                    attack = False
                if event.key == K_p:
                    ability = False

            if pause_menu > 4:
                pause_menu = 4
            if pause_menu < 1:
                pause_menu = 1

        if not _isAlive:
            screen.blit(transparent_death, (0, 0))

            screen.blit(pygame.transform.scale(load_image("game_over.png"), (300, 100)), (460, 250))
            screen.blit(bacK_label, (430, 420))

            if _is_music_pause:
                pygame.mixer.music.stop()
                #print(2)
                battle_music(_isLive=False)
                _is_music_pause = False
        else:
            if global_pause:
                if not use_pause:
                    screen.blit(transparent_pause, (0, 0))
                    screen.blit(pause_label, (475, 50))
                    use_pause = True
                if pause_menu == 1:
                    continue_label = label_font.render('Continue', False, (170, 170, 170))
                    save_label = label_font.render('Save the game', False, (255, 255, 255))
                    options_label = label_font.render('Options', False, (255, 255, 255))
                    exit_label = label_font.render('Back to menu', False, (255, 255, 255))
                if pause_menu == 2:
                    if green_label:
                        save_label = label_font.render('Save the game', False, (80, 255, 80))
                    else:
                        save_label = label_font.render('Save the game', False, (170, 170, 170))
                    continue_label = label_font.render('Continue', False, (255, 255, 255))
                    options_label = label_font.render('Options', False, (255, 255, 255))
                    exit_label = label_font.render('Back to menu', False, (255, 255, 255))
                if pause_menu == 3:
                    continue_label = label_font.render('Continue', False, (255, 255, 255))
                    save_label = label_font.render('Save the game', False, (255, 255, 255))
                    options_label = label_font.render('Options', False, (170, 170, 170))
                    exit_label = label_font.render('Back to menu', False, (255, 255, 255))
                if pause_menu == 4:
                    continue_label = label_font.render('Continue', False, (255, 255, 255))
                    save_label = label_font.render('Save the game', False, (255, 255, 255))
                    options_label = label_font.render('Options', False, (255, 255, 255))
                    exit_label = label_font.render('Back to menu', False, (170, 170, 170))
                screen.blit(continue_label, (540, 300))
                screen.blit(save_label, (475, 370))
                screen.blit(options_label, (547, 440))
                screen.blit(exit_label, (493, 510))

            else:
                screen.blit(bg_castle, (0, 0))
                screen.blit(transparent_surface, (0, 0))
                x_hero, x_origin, y_hero = hero.get_x_y()
                # print(x_hero, y_hero)
                hero.update(x_origin, y_hero, left, right, up, attack, ability, platforms)  # передвижение
                camera.update(hero)  # центризируем камеру относительно персонажа

                boss.boss_behavior(x_hero, y_hero, platforms)

                # _____________________________________-DAMAGE CALCULATING-_______________________________

                # ___________________________________-FROM HERO-_______________________________

                hero_damage, damage_delta = hero.make_damage()
                hero.give_damage(boss.get_tick_damage())
                now_hero_hp, max_hero_hp = hero.get_hp()
                hero_hp.update(int(now_hero_hp), int(max_hero_hp), camera.state.x)
                boss.dam_hero(hero_damage, x_hero, damage_delta)

                # ___________________________________-FROM HERO-_______________________________

                # _____________________________________-DAMAGE CALCULATING-_______________________________
                fps_label.update_fps(int(clock.get_fps()), camera.state.x)

                for element in entities:
                    screen.blit(element.image, camera.apply(element))

                screen.blit(pygame.transform.scale(hero.image, (120, 64)), camera.apply(hero))
                # screen.blit(pygame.transform.scale2x(hero.image), camera.apply(hero))
                # screen.blit(hero.image, camera.apply(hero))

                if now_hero_hp <= 0:
                    _isAlive = False

            if save_flag:
                save_game(x_origin, y_hero, now_hero_hp, json_dict)
                green_label = True
                save_flag = False

        pygame.display.update()  # обновление и вывод всех изменений на экран
        pygame.display.flip()
