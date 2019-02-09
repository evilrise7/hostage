# Надо их по иерхархии типа выстраивать, по комментариям Алексея.
import os
import sys
import random
import datetime

import pygame as pg

# Чтобы окно появлялось по середине экрана
os.environ['SDL_VIDEO_CENTERED'] = '1'
# Инициализация PyGame(назвал, как pg, чтобы укоротить и не получить PEP8)
pg.init()
pg.mixer.init()

# Название и иконка игры
pg.display.set_caption("Hell Obtained Sensible Tiny And Geniusly Emmy.")
pg.display.set_icon(pg.image.load("sprites/icon.png"))

# Разрешение экрана и залипание клавиш(для передвижения игрока в игре)
W_WINDOW = 640
H_WINDOW = 512
screen = pg.display.set_mode((W_WINDOW, H_WINDOW), pg.RESIZABLE)
pg.key.set_repeat(500, 10)

# Три варианта текста, которых достаточно для оформления меню
logo_text = pg.font.Font('cyr.ttf', int(H_WINDOW * 0.15625))
menu_text = pg.font.Font('cyr.ttf', int(H_WINDOW * 0.0703125))
start_menu_text = pg.font.Font('cyr.ttf', int(H_WINDOW * 0.09375))

# Группы спрайтов. Я оформил их отдельно, чтобы изменять поле игры
all_sprites = pg.sprite.Group()
tiles_group = pg.sprite.Group()
secret_group = pg.sprite.Group()
entities_group = pg.sprite.Group()
inventory_group = pg.sprite.Group()
drop_group = pg.sprite.Group()
animal_group = pg.sprite.Group()
particle_group = pg.sprite.Group()

# Звук клика в меню
click_sound = pg.mixer.Sound("sounds/walk.wav")

# Звук подбора вещей в игре
pick_up_sound = pg.mixer.Sound("sounds/pickup.wav")

# Звук пожирания мира
world_cut_sound = pg.mixer.Sound("sounds/cut.wav")

# Звук уничтожения природных объектов(трава, камень, цветки и кусты)
entities_destroy = pg.mixer.Sound("sounds/pick.wav")

# Звук удара коровки
hit_sound = pg.mixer.Sound("sounds/hit.wav")

# Звук "быстрого убийства"
cow_died = pg.mixer.Sound("sounds/cow_died.wav")

volume = True  # Состояние вкл/выкл звуковых эффектов


# Изменение размеров с соотношением размеров экрана
def change_font_size():
    global logo_text, menu_text, start_menu_text
    logo_text = pg.font.Font('cyr.ttf', int(H_WINDOW * 0.15625))
    menu_text = pg.font.Font('cyr.ttf', int(H_WINDOW * 0.0703125))
    start_menu_text = pg.font.Font('cyr.ttf', int(H_WINDOW * 0.09375))


# Функция для загрузки спрайтов
def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Хьюстон, у нас проблемы с ', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


# Проверка выключенных или включенных эффектов
def enable_sfx():
    if volume:
        hit_sound.set_volume(0.5)
        entities_destroy.set_volume(0.4)
        world_cut_sound.set_volume(7.0)
        pick_up_sound.set_volume(1)
        cow_died.set_volume(1)
        click_sound.set_volume(0.4)
    else:
        hit_sound.set_volume(0)
        entities_destroy.set_volume(0)
        pick_up_sound.set_volume(0)
        cow_died.set_volume(0)
        click_sound.set_volume(0)


# Перезагрузка/Очистка всех групп спрайтов
def clear_tiles():
    entities_group.empty()
    tiles_group.empty()
    all_sprites.empty()
    animal_group.empty()
    drop_group.empty()
    inventory_group.empty()


# Кордировщик для честности
def coder(score_output):
    score_output = score_output.replace("0", "Z")
    score_output = score_output.replace("1", "#")
    score_output = score_output.replace("2", "@")
    score_output = score_output.replace("3", "B")
    score_output = score_output.replace("4", "F")
    score_output = score_output.replace("5", "T")
    score_output = score_output.replace("6", "N")
    score_output = score_output.replace("7", "Q")
    score_output = score_output.replace("8", "X")
    score_output = score_output.replace("9", "W")
    score_output = score_output.replace(":", "/")
    return score_output


# Перекордировщик для честности
def decoder(score_input):
    score_input = score_input.replace("Z", "0")
    score_input = score_input.replace("#", "1")
    score_input = score_input.replace("@", "2")
    score_input = score_input.replace("B", "3")
    score_input = score_input.replace("F", "4")
    score_input = score_input.replace("T", "5")
    score_input = score_input.replace("N", "6")
    score_input = score_input.replace("Q", "7")
    score_input = score_input.replace("X", "8")
    score_input = score_input.replace("W", "9")
    score_input = score_input.replace("/", ":")
    return score_input


def window_resizing(event):
    global W_WINDOW, H_WINDOW, screen
    if event.w > 639 and event.h > 511:
        W_WINDOW = event.w
        H_WINDOW = event.h
        screen = pg.display.set_mode((W_WINDOW, H_WINDOW), pg.RESIZABLE)
    else:
        screen = pg.display.set_mode((640, 512), pg.RESIZABLE)


def put_logo(screen):
    # Логотип игры
    logo = load_image("logo.png")
    logo = pg.transform.scale(logo, (int(W_WINDOW * 0.225),
                                     int(W_WINDOW * 0.225 / 0.773)))
    # Добавить спрайты на экран
    pos_logo = H_WINDOW // 2 - logo.get_rect().size[1] // 2
    screen.blit(logo, (W_WINDOW * 0.625, pos_logo))


# Словарь спрайтов игрового мира
tile_images = {"grass": load_image('grass.png'),
               "sand": load_image('sand.png'),
               "stone": load_image('stone.png'),
               "empty": load_image('empty_tile.png')}

# Словарь спрайтов секретного уровня
secret_images = {"bath": load_image('bath.png'),
                 "shower": load_image('shower.png'),
                 "right_eye": load_image('eye2.png'),
                 "left_eye": load_image('eye1.png'),
                 "victim1": load_image('victim1.png'),
                 "victim2": load_image('victim2.png'),
                 "victim3": load_image('victim3.png'),
                 "victim4": load_image('victim4.png'),
                 "victim5": load_image('victim5.png')}

# Словарь спрайтов природных объектов
entity_images = {"green": load_image('green.png'),
                 "flowers": load_image('flowers.png'),
                 "rock": load_image('rock.png'),
                 "bush": load_image('bush.png'),
                 "meat": load_image('meat_entity.png'),
                 "gold_sword": load_image('gold_sword_entity.png'),
                 "silver_sword": load_image('silver_sword_entity.png'),
                 "blood": load_image('blood_entity.png')}

# Словарь спрайтов инвентаря
inventory_images = {"empty": load_image('empty.png'),
                    "meat_block": load_image('meat_block_inv.png'),
                    "eyes": load_image('eyes_inv.png'),
                    "meat": load_image('meat_inv.png'),
                    "gold": load_image('gold_inv.png'),
                    "gold_sword": load_image('gold_sword_inv.png'),
                    "silver_sword": load_image('silver_sword_inv.png'),
                    "victim1": load_image('victim1_inv.png'),
                    "victim2": load_image('victim2_inv.png'),
                    "victim3": load_image('victim3_inv.png'),
                    "victim4": load_image('victim4_inv.png'),
                    "victim5": load_image('victim5_inv.png')}

# Словарь спрайтов выпавших вещей
drop_images = {"meat": load_image('meat.png'),
               "gold": load_image('gold.png'),
               "eyes": load_image('eyes.png'),
               "gold_sword": load_image('gold_sword.png'),
               "silver_sword": load_image('silver_sword.png'),
               "meat_block": load_image('meat_block.png')}

# Переменная отвечает за запуск секретного уровня
psycho_level = 0
# Переменная ограничитель для частиц
screen_rect = (0, 0, 4224, 4224)


# Класс меню
class Menu:
    def __init__(self):
        self.running = True
        pg.mouse.set_visible(True)  # Сделать мышь видимой
        # Начать игру, Результаты, Настройки и Выход
        self.button_init()

    def button_init(self):
        self.start_game = menu_text.render("Start Game", 0, (100, 100, 100))
        self.record_txt = menu_text.render("Scores", 0, (100, 100, 100))
        self.settings_txt = menu_text.render("Settings", 0, (100, 100, 100))
        self.exit_txt = menu_text.render("Quit", 0, (100, 100, 100))

    def resize_rect_button(self):
        global W_WINDOW, H_WINDOW, screen
        # Начать игру, Результаты, Настройки и Выход
        self.start_game_rect = self.start_game.get_rect().move(W_WINDOW * 0.125,
                                                               H_WINDOW * 0.29296875)
        self.record_rect = self.record_txt.get_rect().move(W_WINDOW * 0.125,
                                                           H_WINDOW * 0.390625)
        self.settings_rect = self.settings_txt.get_rect().move(W_WINDOW * 0.125,
                                                               H_WINDOW * 0.48828125)
        self.exit_rect = self.exit_txt.get_rect().move(W_WINDOW * 0.125,
                                                       H_WINDOW * 0.5859375)

    def run(self):
        global W_WINDOW, H_WINDOW, screen
        self.resize_rect_button()
        enable_sfx()  # Проверка Вкл/Выкл звуковых эффектов
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False  # Выход из игры, при закрытии окна

                # Адаптация всех объектов при расширении экрана
                if event.type == pg.VIDEORESIZE:
                    window_resizing(event)
                    change_font_size()
                    self.button_init()
                    self.resize_rect_button()

                # "Анимированные" тексты кнопок меню
                if event.type == pg.MOUSEMOTION:
                    if self.start_game_rect.collidepoint(event.pos):
                        self.start_game = menu_text.render(
                            "Start Game", 0, (255, 255, 255))
                    else:
                        self.start_game = menu_text.render(
                            "Start Game", 0, (100, 100, 100))

                    if self.record_rect.collidepoint(event.pos):
                        self.record_txt = menu_text.render(
                            "Scores", 0, (255, 255, 255))
                    else:
                        self.record_txt = menu_text.render(
                            "Scores", 0, (100, 100, 100))

                    if self.settings_rect.collidepoint(event.pos):
                        self.settings_txt = menu_text.render(
                            "Settings", 0, (255, 255, 255))
                    else:
                        self.settings_txt = menu_text.render(
                            "Settings", 0, (100, 100, 100))

                    if self.exit_rect.collidepoint(event.pos):
                        self.exit_txt = menu_text.render(
                            "Quit", 0, (255, 255, 255))
                    else:
                        self.exit_txt = menu_text.render(
                            "Quit", 0, (100, 100, 100))

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.start_game_rect.collidepoint(event.pos):
                        # Запуск меню выбора уровней
                        click_sound.play()
                        Level().run()

                    if self.record_rect.collidepoint(event.pos):
                        click_sound.play()
                        Score().run()
                    if self.settings_rect.collidepoint(event.pos):
                        click_sound.play()
                        Settings().run()
                    if self.exit_rect.collidepoint(event.pos):
                        # Выход из игры
                        click_sound.play()
                        self.running = False
            # Обновления кадра, путем заливки
            screen.fill((0, 0, 0))
            # Логотипы
            game_logo_text = logo_text.render("H.O.S.T.A.G.E.",
                                              0, (255, 255, 255))
            put_logo(screen)
            screen.blit(self.start_game, (W_WINDOW * 0.125,
                                          H_WINDOW * 0.29296875))
            screen.blit(self.record_txt, (W_WINDOW * 0.125,
                                          H_WINDOW * 0.390625))
            screen.blit(self.settings_txt, (W_WINDOW * 0.125,
                                            H_WINDOW * 0.48828125))
            screen.blit(self.exit_txt, (W_WINDOW * 0.125,
                                        H_WINDOW * 0.5859375))
            screen.blit(game_logo_text, (W_WINDOW * 0.125,
                                         H_WINDOW * 0.05859375))
            # Обновление кадра
            pg.display.flip()
        # Выход из игры
        pg.quit()
        sys.exit()


# Выбор уровней
class Level:
    def __init__(self):
        self.running = True
        self.level = psycho_level  # Проверка секретного уровня
        # Загрузка спрайтов выбора уровней
        self.level_terrain = load_image("level1.png")
        self.level_secret = load_image("level2.png")
        self.txt_init()

    def txt_init(self):
        self.choose_level_txt = start_menu_text.render(
            "CHOOSE YOUR LEVEL!", 0, (255, 255, 255))

    def run(self):
        global W_WINDOW, H_WINDOW, screen

        while self.running:
            change_font_size()  # Адаптация шрифта
            # Позиция уровней по OY
            pos_lvl_terrain = H_WINDOW // 2 - self.level_terrain.get_rect().size[1] // 2
            pos_secret = H_WINDOW // 2 - self.level_secret.get_rect().size[1] // 2

            # Маски спрайтов из прямоугольника для клика
            self.level_terrain_rect = self.level_terrain.get_rect().move(
                0, pos_lvl_terrain)
            self.level_secret_rect = self.level_secret.get_rect().move(
                W_WINDOW // 2, pos_secret)

            for event in pg.event.get():
                # Закрытие экрана
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False
                # При расширении экрана
                if event.type == pg.VIDEORESIZE:
                    window_resizing(event)
                    change_font_size()
                    self.txt_init()

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Запустить обычный игровой мир
                    if self.level_terrain_rect.collidepoint(event.pos):
                        click_sound.play()
                        TutorialTerrain().run()
                    # Запустить секретный уровень
                    if self.level_secret_rect.collidepoint(
                            event.pos) and self.level == 1:
                        click_sound.play()
                        SecretLevel().run()

            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Размеры картинок уровней
            self.level_terrain = pg.transform.scale(self.level_terrain,
                                                    (W_WINDOW // 2,
                                                     int(W_WINDOW // 2 * 0.8)))
            self.level_secret = pg.transform.scale(self.level_secret,
                                                   (W_WINDOW // 2,
                                                    int(W_WINDOW // 2 * 0.8)))
            # Добавление объектов на экран
            screen.blit(self.choose_level_txt,
                        (W_WINDOW // 2 - self.choose_level_txt.get_width() // 2,
                         H_WINDOW * 0.0390625))
            screen.blit(self.level_terrain, (0, pos_lvl_terrain))
            # Если секретный уровень открыт, добавить его выбор на экран
            if self.level:
                screen.blit(self.level_secret, (W_WINDOW // 2, pos_secret))
            # Обновление кадра
            pg.display.flip()
        # Запуск меню
        open_menu()


# Результаты
class Score:
    def __init__(self):
        self.running = True
        self.score_list = []  # Лист рекордов

    def top5scores(self):
        # Отступ для рекордов
        liney = H_WINDOW * 0.3125
        # Чтение всех строк из файла с рекордами
        with open('score.txt', 'r') as score_file:
            self.score_list = [line.strip() for line in score_file]

        if not self.score_list or self.score_list[0] == "":
            # Если отсутсвуют рекорды, то пишется текст "Пусто"
            screen.blit(menu_text.render(
                "Empty", 0, (255, 255, 255)), (W_WINDOW * 0.234375,
                                               H_WINDOW * 0.29296875))

        # Если рекорды присутствуют
        else:
            # Сортирую для топа
            self.score_list.sort()
            # Вырезаю первые 5 рекордов, если длина листа превышает 5
            if len(self.score_list) > 5:
                self.score_list = self.score_list[0:5]

            for i in range(len(self.score_list)):
                # Перекодировщик рекорда
                self.score_list[i] = decoder(self.score_list[i])
                # Добавления самих рекордов
                screen.blit(menu_text.render(
                    str(i + 1) + ". " + str(self.score_list[i]),
                    0, (255, 255, 255)), (W_WINDOW * 0.15625, liney))
                liney += H_WINDOW * 0.05859375  # Добавление отсутпа

    def run(self):
        enable_sfx()  # Проверка Вкл/Выкл звуковых эффектов
        while self.running:
            for event in pg.event.get():
                # Выход из игры, при закрытии окна
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False

                if event.type == pg.VIDEORESIZE:
                    window_resizing(event)
                    change_font_size()

                # Выход из игры нажатием ESC
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            # Обновления кадра, путем заливки
            screen.fill((0, 0, 0))
            # Заголовок Результаты
            self.score_title = menu_text.render("TOP 5 SPEEDRUNS:",
                                                0, (255, 255, 255))
            put_logo(screen)
            screen.blit(self.score_title, (W_WINDOW * 0.125,
                                           H_WINDOW * 0.1953125))
            self.top5scores()
            # Обновление кадра
            pg.display.flip()
        # Перейти в меню
        open_menu()


# Настройки
class Settings:
    def __init__(self):
        self.running = True  # Когда окно действует
        self.button_init(volume)

    def button_init(self, volume):
        # Заголовок Настроек, Звуковых эффектов и Сброса Результатов
        self.settings_title = menu_text.render("SETTINGS", 0, (255, 255, 255))

        if volume:
            self.volume_title = menu_text.render(
                "SOUND EFFECTS: ON", 0, (255, 255, 255))
        else:
            self.volume_title = menu_text.render(
                "SOUND EFFECTS: OFF", 0, (255, 255, 255))
        self.volume_rect = self.volume_title.get_rect().move(W_WINDOW * 0.125,
                                                             H_WINDOW * 0.390625)

        self.record_title = menu_text.render("RESET SCORES", 0, (255, 255, 255))
        self.record_rect = self.record_title.get_rect().move(W_WINDOW * 0.125,
                                                             H_WINDOW * 0.5859375)

    def run(self):
        global volume

        while self.running:
            for event in pg.event.get():
                # Выход из игры, при закрытии окна
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False

                if event.type == pg.VIDEORESIZE:
                    window_resizing(event)
                    change_font_size()

                # Выход из игры нажатием ESC
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                # Когда кликаем на текст про звуковые эффекты
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.volume_rect.collidepoint(event.pos):
                        # Смена звуковых эффектов
                        click_sound.play()
                        if volume:
                            volume = False
                        else:
                            volume = True
                        enable_sfx()  # Проверка Вкл/Выкл звуковых эффектов

                    if self.record_rect.collidepoint(event.pos):
                        # Сброс результатов
                        click_sound.play()
                        open('score.txt', 'w').close()

            # Обновления кадра, путем заливки
            screen.fill((0, 0, 0))
            put_logo(screen)
            self.button_init(volume)
            screen.blit(self.settings_title, (W_WINDOW * 0.125,
                                              H_WINDOW * 0.1953125))
            screen.blit(self.volume_title, (W_WINDOW * 0.125,
                                            H_WINDOW * 0.390625))
            screen.blit(self.record_title, (W_WINDOW * 0.125,
                                            H_WINDOW * 0.5859375))
            # Обновление кадра
            pg.display.flip()
        # Перейти в меню
        open_menu()


# Туториал для игрового мира
class TutorialTerrain:
    def __init__(self):
        self.running = True
        self.slide = 1  # Текущий слайд туториала
        # Если игрок не нажимает на слайд
        # надпись "click" остается
        self.show = False

    def run(self):
        enable_sfx()  # Проверка Вкл/Выкл звуковых эффектов
        while self.running:
            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Переключение слайдов
                    if self.slide < 9:
                        # Конечный слайд заменяется на первый
                        self.slide += 1
                    else:
                        self.slide = 1
                    # Убрать надпись "Click"
                    self.show = True
                    click_sound.play()

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                    # любая другая кнопка, активирует меню персонажа
                    else:
                        click_sound.play()
                        StartMenu().run()

                if event.type == pg.VIDEORESIZE:
                    window_resizing(event)
            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Добавление слайдов и их расположение
            slide_img = load_image("t" + str(self.slide) + ".png")
            slide_img = pg.transform.scale(slide_img, (int(H_WINDOW / 0.8),
                                                       H_WINDOW))
            slidex = W_WINDOW // 2 - slide_img.get_rect().size[0] // 2
            slidey = H_WINDOW // 2 - slide_img.get_rect().size[1] // 2
            screen.blit(slide_img, (slidex, slidey))
            if not self.show:
                screen.blit(
                    start_menu_text.render("Click to slide",
                                           0, (255, 255, 255)), (slidex, slidey))
            # Обновление кадра
            pg.display.flip()
        # Переход в меню
        open_menu()


# Меню выбора персонажей
class StartMenu:
    def __init__(self):
        self.running = True
        self.gender = ""    # Половая принадлежность
        self.difficult = ""  # Сложность игры
        # Картинки персонажей и текст " Выбрать персонажа "
        self.martin_image = load_image("p.png")
        self.margo_image = load_image("f.png")
        self.objects_init()

    def objects_init(self):
        # Отступы слева
        self.leftx = W_WINDOW * 0.15625
        self.leftx_dif = W_WINDOW * 0.09375

        # Персонаж Мартин и его прямоугольная маска
        self.martin_txt = start_menu_text.render(
            "MARTIN", 0, (100, 100, 100))
        self.martin_rect = self.martin_txt.get_rect().move(
            self.leftx, H_WINDOW * 0.546875)

        # Персонаж Марго и ее прямоугольная маска
        self.margo_txt = start_menu_text.render(
            "MARGO", 0, (100, 100, 100))
        self.rightx = W_WINDOW - self.leftx - self.margo_txt.get_width()
        self.margo_rect = self.margo_txt.get_rect().move(
            self.rightx, H_WINDOW * 0.546875)

        # Легкая сложность
        self.easy_txt = start_menu_text.render(
            "EASY", 0, (100, 100, 100))
        self.easy_rect = self.easy_txt.get_rect().move(
            self.leftx_dif, H_WINDOW * 0.78125)

        # Средняя сложность
        self.medium_txt = start_menu_text.render(
            "MEDIUM", 0, (100, 100, 100))
        self.medium_x = W_WINDOW // 2 - self.medium_txt.get_width() // 2
        self.medium_rect = self.medium_txt.get_rect().move(
            self.medium_x, H_WINDOW * 0.78125)

        # Высокая сложность
        self.hardcore_txt = start_menu_text.render(
            "HARD", 0, (100, 100, 100))
        self.rightx_dif = W_WINDOW - self.leftx_dif - self.hardcore_txt.get_width()
        self.hardcore_rect = self.hardcore_txt.get_rect().move(
            self.rightx_dif, H_WINDOW * 0.78125)

        # Изменение размеров картинок игроков
        self.hero_size = int(H_WINDOW * 0.3828125)
        self.martin_image = pg.transform.scale(
            self.martin_image, (self.hero_size, self.hero_size))
        self.margo_image = pg.transform.scale(
            self.margo_image, (self.hero_size, self.hero_size))

        # Заголовок
        self.press_to_start = start_menu_text.render(
            "CHOOSE A CHARACTER!", 0, (255, 255, 255))
        self.start_txt_x = W_WINDOW // 2 - self.press_to_start.get_width() // 2

        # Анимация текстов
        self.animated_txt()

    def animated_txt(self):
        # Анимация текстов Персонажей
        if self.gender == "female":
            self.margo_txt = start_menu_text.render(
                "MARGO", 0, (255, 255, 255))

        if self.gender == "male":
            self.martin_txt = start_menu_text.render(
                "MARTIN", 0, (255, 255, 255))

        # Анимация сложностей
        if self.difficult == "easy":
            self.easy_txt = start_menu_text.render(
                "EASY", 0, (255, 255, 255))

        if self.difficult == "medium":
            self.medium_txt = start_menu_text.render(
                "MEDIUM", 0, (255, 255, 255))

        if self.difficult == "hardcore":
            self.hardcore_txt = start_menu_text.render(
                "HARD", 0, (255, 255, 255))

    def run(self):
        enable_sfx()  # Проверка Вкл/Выкл звуковых эффектов
        while self.running:
            for event in pg.event.get():
                # Закрыть окно
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False

                # Расширение экрана
                if event.type == pg.VIDEORESIZE:
                    window_resizing(event)
                    change_font_size()

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                    # Запуск игры
                    if event.key == pg.K_SPACE:
                        if self.difficult != "" and self.gender != "":
                            Game(difficult=self.difficult,
                                 boyorgirl=self.gender).run()

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Выбор Мартина
                    if self.martin_rect.collidepoint(event.pos):
                        self.gender = "male"
                        click_sound.play()
                    # Выбор Марго
                    if self.margo_rect.collidepoint(event.pos):
                        self.gender = "female"
                        click_sound.play()

                    if self.gender:
                        # Если игрок выбрал персонажа, то сложности активны
                        if self.easy_rect.collidepoint(event.pos):
                            self.difficult = "easy"
                            click_sound.play()
                        if self.medium_rect.collidepoint(event.pos):
                            self.difficult = "medium"
                            click_sound.play()
                        if self.hardcore_rect.collidepoint(event.pos):
                            self.difficult = "hardcore"
                            click_sound.play()
            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            self.objects_init()
            # Добавление объектов на экран
            # self.hero_size/5 - чтобы выравнить картинки по центру текста
            screen.blit(self.martin_image, (self.leftx - self.hero_size / 5,
                                            H_WINDOW * 0.15625))
            screen.blit(self.margo_image, (self.rightx - self.hero_size / 5,
                                           H_WINDOW * 0.15625))

            screen.blit(self.martin_txt, (self.leftx,
                                          H_WINDOW * 0.546875))
            screen.blit(self.margo_txt, (self.rightx,
                                         H_WINDOW * 0.546875))

            screen.blit(self.easy_txt, (self.leftx_dif,
                                        H_WINDOW * 0.78125))
            screen.blit(self.medium_txt, (self.medium_x, H_WINDOW * 0.78125))
            screen.blit(self.hardcore_txt, (self.rightx_dif,
                                            H_WINDOW * 0.78125))

            # Если игрок выбрал все, что ему нужно
            if self.difficult != "" and self.gender != "":
                self.press_to_start = start_menu_text.render(
                    "PRESS SPACE TO BEGIN!", 0, (255, 255, 255))

            # Если игрок выбрал персонажа
            elif self.difficult == "" and self.gender:
                self.press_to_start = start_menu_text.render(
                    "CHOOSE DIFFUCLTY!", 0, (255, 255, 255))

            # Добавление заголовка выбора сложности и игрока
            screen.blit(self.press_to_start, (self.start_txt_x, 0))
            # Обновление кадра
            pg.display.flip()
        # Переход в меню
        open_menu()


# Окно проигрыша
class GameOver:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                # Расширение экрана
                if event.type == pg.VIDEORESIZE:
                    window_resizing(event)
                    change_font_size()

            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            if psycho_level:
                children_txt = start_menu_text.render(
                    "Children.", 0, (255, 0, 0))
                txt_x = W_WINDOW // 2 - children_txt.get_width() // 2
                txt_y = H_WINDOW // 2 - children_txt.get_height() // 2
                # Если открыт секретный уровень, будет изменен текст дети
                screen.blit(children_txt, (txt_x, txt_y))
            else:
                game_over_txt = start_menu_text.render(
                    "Game Over", 0, (255, 0, 0))
                txt_x = W_WINDOW // 2 - game_over_txt.get_width() // 2
                txt_y = H_WINDOW // 2 - game_over_txt.get_height() // 2
                # Если не открыт, будет изменен текст проигрыша
                screen.blit(game_over_txt, (txt_x, txt_y))
            # Обновление кадра
            pg.display.flip()
        # Перейти в меню
        open_menu()


# Выигрыш игры
class Win:
    def __init__(self, score, difficult):
        self.running = True
        self.score = score  # Время прохождения игры
        self.difficult = difficult  # Сложность игры

    def run(self):
        # Запись результата в текстовый документ
        output_score = open("score.txt", "a")
        # Кодирование результатов и запись
        writing_score = coder(self.score)
        output_score.write(str(
            writing_score) + " " + self.difficult + "\n")
        output_score.close()
        while self.running:
            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Добавление объектов на экран
            screen.blit(start_menu_text.render(
                "You win!", 0, (0, 255, 0)), (210, 200))
            screen.blit(menu_text.render(
                "Your time is", 0, (255, 255, 255)), (200, 250))
            screen.blit(menu_text.render(
                str(self.score), 0, (255, 255, 255)), (250, 290))
            # Обновление кадра
            pg.display.flip()
        # Запуск меню, при выходе
        open_menu()


# Выигрыш секретного уровня
class DrownedChildren:
    def __init__(self):
        self.running = True

    def run(self):
        # Загрузка объектов
        child_d = load_image("child_D.png")
        child_d = pg.transform.scale(child_d, (144, 144))

        child_r = load_image("child_R.png")
        child_r = pg.transform.scale(child_r, (144, 144))

        child_o = load_image("child_O.png")
        child_o = pg.transform.scale(child_o, (144, 144))

        child_w = load_image("child_W.png")
        child_w = pg.transform.scale(child_w, (144, 144))

        child_n = load_image("child_N.png")
        child_n = pg.transform.scale(child_n, (144, 144))
        while self.running:
            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Добавление объектов на экран
            screen.blit(child_d, (60, 70))
            screen.blit(child_r, (156, 70))
            screen.blit(child_o, (252, 70))
            screen.blit(child_w, (348, 70))
            screen.blit(child_n, (444, 70))

            screen.blit(start_menu_text.render("Congratulations!", 0,
                                               (255, 255, 255)), (130, 230))
            screen.blit(start_menu_text.render("You drowned your own", 0,
                                               (255, 255, 255)), (40, 270))
            screen.blit(start_menu_text.render("children.", 0,
                                               (255, 255, 255)), (220, 310))
            screen.blit(start_menu_text.render("You're the best mother!", 0,
                                               (255, 255, 255)), (20, 350))
            # Обновление кадра
            pg.display.flip()
        # Запуск меню
        open_menu()


# Игровой мир (Уровень 1)
class Game:
    def __init__(self, difficult="easy", boyorgirl="male"):
        self.running = True
        # Очистить все поле, при старте новой игры
        clear_tiles()
        # Текущий инструмент == Топор
        self.tool = "axe"
        # Пауза
        self.pause = False
        self.dt = 0  # Обновление времени внутри системы
        self.FPS = 100  # Кадры в секунду для оптимизации
        self.clock = pg.time.Clock()  # Часы внутренние
        self.timer_cut = 0  # Время поедания мира
        self.time_in_game = 0  # Игровое время прохождения
        self.difficult = difficult  # Сложность игры
        self.step = 1  # Пожирание N клеток границ
        # Текущий игровой мир(карта)
        self.world = TileMap()
        # Текущий инвентарь игрового мира
        self.inventory = Inventory()

        posx = 0  # Положение игрока в матрице игрового мира по оси Ox
        posy = 0  # Положение игрока в матрице игрового мира по оси Oy

        self.gold = 0  # Количество золота
        self.silver_sword = 0  # Вероятность выпадения серебрянного меча
        # Вероятности выпадения мечей
        self.is_gold_sword = random.randint(0, 100)
        self.is_silver_sword = random.randint(0, 100)
        self.gold_sword = 0  # Количество золотых мечей

        # В какой четверти мира появится игрок
        quarter = random.randint(1, 4)

        if quarter == 1:  # I-я четверть
            posx = random.randint(1, 15)
            posy = random.randint(1, 15)

        if quarter == 2:  # II-я четверть
            posx = random.randint(16, 31)
            posy = random.randint(16, 31)

        if quarter == 3:  # III-я четверть
            posx = random.randint(32, 47)
            posy = random.randint(32, 47)

        if quarter == 4:  # IV-я четверть
            posx = random.randint(48, 62)
            posy = random.randint(48, 62)

        # Создание игрока
        self.player = Player(all_sprites, self, posx - 0.5,
                             posy - 0.5, 64, boyorgirl)
        self.camera = Camera()  # Создание камеры
        self.inventory = Inventory()  # Создание инвентаря
        self.craft = Craft()  # Создания кравта

        self.mobs = []  # Лист живых существ
        for _ in range(random.randint(18, 24)):
            self.mobs.append(Cow(animal_group,
                                 self, random.randint(2, 62),
                                 random.randint(2, 62), 64))
        self.drop = []
        self.tmpmobs = []  # Буферный лист живых существ
        # Лист, чтобы прослеживать уже добавленные предметы
        self.tmplist = []

        # Установка интервала пожирания границ мира,
        # в зависимости от сложности
        if self.difficult == "easy":
            self.cell_timer = 15
        if self.difficult == "medium":
            self.cell_timer = 7.5
        if self.difficult == "hardcore":
            self.cell_timer = 3.75
        # Загрузка курсора инвентаря и его позиция
        self.current_cursor_pos = 0
        self.cursor = load_image("cursor.png")
        self.cursor = pg.transform.scale(self.cursor, (72, 72))

    def player_run(self):
        # Обработка бегающего игрока
        self.player.state = "run"
        self.player.timer = 0.05
        self.gender()

    def gender(self):
        # Обработка пола игрока
        if self.player.gender == "male":  # Мартин
            if self.player.mirrored:
                self.player.cut_sheet(load_image("pm_sheet.png"))
            else:
                self.player.cut_sheet(load_image("p_sheet.png"))

        else:  # Марго
            if self.player.mirrored:
                self.player.cut_sheet(load_image("fm_sheet.png"))
            else:
                self.player.cut_sheet(load_image("f_sheet.png"))

    def player_stay(self):
        # Обработка стоячего игрока
        self.player.state = "stay"
        self.player.timer = 0.5
        self.gender()

    def update_tiles(self):
        # Обновление всех спрайтов вдоль камеры
        for sprite in tiles_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in entities_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in animal_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in all_sprites:
            pos = self.camera.apply(sprite)
            # Отображаю инструмент игрока относительно него
            if not sprite.mirrored:
                tool_img = load_image("tool_" + str(self.tool) + ".png")
                tool_img = pg.transform.scale(tool_img, (72, 72))
                screen.blit(tool_img, (pos[0] - 28, pos[1] - 4))

            if sprite.mirrored:
                tool_img = load_image("toolm_" + str(self.tool) + ".png")
                tool_img = pg.transform.scale(tool_img, (72, 72))
                screen.blit(tool_img, (pos[0] + 24, pos[1] - 4))

            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in particle_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in drop_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in animal_group:
            # Отображаю жизни животных
            pos = self.camera.apply(sprite)
            if sprite.hp:
                screen.blit(menu_text.render(
                    str(sprite.hp) + "HP", 0, (255, 255, 255)),
                    (pos[0], pos[1] - 40))

    def world_cutting(self):
        # Если таймер уничтожения границ больше, чем
        # заданное время уничтожения границ по сложности
        # мир пожирается по краям
        self.timer_cut += self.dt
        if self.timer_cut > self.cell_timer:
            self.step += 1  # Пожирание N границ увеличивается
            # Пожирание границ,
            # путем изменения значений в матрице
            for i in range(self.world.w):
                self.world.world_array[self.step - 1][i] = -1
                self.world.world_array[-self.step][i] = -1

            for i in range(self.world.h):
                self.world.world_array[i][self.step - 1] = -1
                self.world.world_array[i][-self.step] = -1

            # Перезагрузка карты игрового мира
            # природных объектов и животных
            self.world.render()

            tiles_group.update()
            entities_group.update()
            animal_group.update()

            world_cut_sound.play()
            self.timer_cut = 0  # Сброс таймера

    def check_cows(self):
        for i in range(len(self.mobs)):
            # Если животное касается границ, то оно отлетает
            if self.mobs[i].rect.x < 64 * self.step:
                self.mobs[i].vx = 0
                self.mobs[i].vx += 72
            if self.mobs[i].rect.x > 64 * (65 - self.step):
                self.mobs[i].vx = 0
                self.mobs[i].vx -= 72
            if self.mobs[i].rect.y < 64 * self.step:
                self.mobs[i].vy = 0
                self.mobs[i].vy += 72
            if self.mobs[i].rect.y > 64 * (65 - self.step):
                self.mobs[i].vy = 0
                self.mobs[i].vy -= 72

    def append_drop(self, x, y):
        b = random.randint(0, 100)  # Вероятность выпадения M-го предмета
        # Если золотой меч имеет вероятность меньше 50%
        # то из природных объектов выпадает золотые слитки
        if self.is_gold_sword < 50:
            if b < 30 and self.gold < 2:
                self.drop.append(Drop("gold", self.player, x, y, self))
                self.gold += 1
        # Если золотой меч имеет вероятность больше или равно 50%
        # то из природных объектов выпадает золотой меч
        if self.is_gold_sword >= 50:
            if b >= 70 and self.gold_sword < 1:
                self.drop.append(Drop("gold_sword", self.player, x, y, self))
                self.gold_sword += 1
        # Если серебрянный меч имеет вероятность больше 50% и 100% появление,
        # то из природных объектов выпадает серебрянный меч
        if self.is_silver_sword >= 50:
            if b == 100 and self.silver_sword < 1:
                self.drop.append(Drop("silver_sword", self.player, x, y, self))
                self.silver_sword += 1

    def append_drop_block(self, x, y, i):
        # Выпадение мясного блока, золотого и серебрянного меча
        if i == 5:
            self.drop.append(Drop("meat_block", self.player, x, y, self))
        if i == 6:
            self.drop.append(Drop("gold_sword", self.player, x, y, self))
        if i == 7:
            self.drop.append(Drop("silver_sword", self.player, x, y, self))

    def cow_and_player(self):
        for i in range(len(self.mobs)):
            # Если живое существо касается героя
            if self.mobs[i].rect.colliderect(self.player.rect):
                # При применении насилия к животным(ну вы поняли)
                # Появляются частицы крови.
                # Если в руках топор, то у коровы отнимается 2 жизни
                if self.tool == "axe":
                    create_particles((self.player.rect.x + 32,
                                      self.player.rect.y + 32))
                    self.mobs[i].hp -= 2
                    hit_sound.play()
                # Если в руках ножницы, то у коровы отнимается 1 жизнь
                else:
                    create_particles((self.player.rect.x + 32,
                                      self.player.rect.y + 32))
                    self.mobs[i].hp -= 1
                    hit_sound.play()

                # Проверка, куда бежать от игрока
                if self.player.rect.y < self.mobs[i].rect.y:
                    self.mobs[i].movement(4)

                if self.player.rect.y > self.mobs[i].rect.y:
                    self.mobs[i].movement(3)

                if self.player.mirrored:
                    self.mobs[i].movement(2)

                if not self.player.mirrored:
                    self.mobs[i].movement(1)

                else:
                    self.mobs[i].movement(random.randint(1, 4))

                self.mobs[i].vx = 0
                self.mobs[i].vy = 0
                self.mobs[i].timer_run = 3

                if self.mobs[i].check_hp():
                    # Беру координаты игрока, т.к. PEP8 ругался
                    # за то, что я писал длинные строки
                    x = int((self.player.rect.x + 32) / 4096 * 64)
                    y = int((self.player.rect.y + 32) / 4096 * 64)
                    # Если живое существо имеет жизни == 0, то оно погибает
                    cow_died.play()
                    self.mobs[i].kill()
                    # Перезагрузка выпавших вещей
                    drop_group.update()
                    # Если в руках топор, то выпадает мясо
                    if self.tool == "axe":
                        self.drop.append(Drop("meat", self.player, x, y, self))
                    # Если в руках ножницы, то выпадают глаза
                    else:
                        self.drop.append(Drop("eyes", self.player, x, y, self))
                    # Буферный лист добавляет соотвествующее животное
                    self.tmpmobs.append(i)
                    if self.world.entities[y][x] < 5:
                        self.world.entities[y][x] = -2
                        self.world.render()
                        entities_group.update()
        # Если буферный лист заполнен,
        # то все животные в этом листе очищаются в основном
        if self.tmpmobs:
            for i in range(len(self.tmpmobs)):
                del self.mobs[self.tmpmobs[i]]
        # Очистка буферного листа животных
        self.tmpmobs.clear()

    def craft_checking(self):
        # Проверка подсказки создания вещей
        for i in range(self.inventory.w):
            # Если в инвентаре есть мясо и глаза,
            # то отображается подсказка
            # создания сухожилия
            if self.inventory.inv[0][i] == "meat" \
                    or self.inventory.inv[0][i] == "eyes":
                if self.current_cursor_pos == i:
                    if self.inventory.check_craft_meat():
                        self.craft.craft_type = 0

            # Если в инвентаре есть золото,
            # то отображается подсказка
            # создания золотого меча
            if self.inventory.inv[0][i] == "gold":
                if self.current_cursor_pos == i:
                    if self.inventory.check_craft_gold():
                        self.craft.craft_type = 1

    def drop_clean(self):
        # Очистка упавших вещей
        if self.drop:
            for i in range(len(self.drop)):
                # При уничтожении, уничтоженный предмет попадает в
                # буферный лист
                if self.drop[i].check_drop_pos() == 1:
                    self.drop[i].kill()
                    self.tmplist.remove(i)

                if self.drop[i].get_event() == 1:
                    self.drop[i].kill()
                    self.inventory.append(self.drop[i].type)
                    self.tmplist.append(i)
        # Если буферный лист забит, то лист упавших вещей
        # удаляет элементы, содержащиеся в буферном листе
        if self.tmplist and self.drop:
            for i in range(len(self.tmplist)):
                del self.drop[self.tmplist[i]]
        # Очистка буферного листа
        self.tmplist.clear()

    def put_block(self, block):
        # Установка предметов из инвентаря
        b = 0
        index1 = 0
        for i in range(self.inventory.w):
            # Если данный предмет присутствует, то
            # берутся индекс и присутсвие предмета из инвентаря
            if self.inventory.inv[0][i] == block and \
                    self.inventory.inv[1][i] > 0:
                b += 1
                index1 = i
        if b:
            # Удаление соотвествующего предмета из инвентаря
            self.inventory.inv[1][index1] -= 1
            if self.inventory.inv[1][index1] == 0:
                self.inventory.invtmp.remove(self.inventory.inv[0][index1])
                self.inventory.inv[0][index1] = 0

    def create_object(self, y, xl, xr):
        for i in range(self.inventory.w):
            # Если в инвентаре есть мясной блок
            # И курсор находится на его позиции
            if self.inventory.inv[0][i] == "meat_block":
                if self.current_cursor_pos == i:
                    # Установка блока в зависимости
                    # От положения игрока
                    if self.player.mirrored:
                        if self.world.entities[y][xr] < 5:
                            self.world.entities[y][xr] = 5
                            self.world.render()
                            entities_group.update()
                            self.put_block("meat_block")
                    else:
                        if self.world.entities[y][xl] < 5:
                            self.world.entities[y][xl] = 5
                            self.world.render()
                            entities_group.update()
                            self.put_block("meat_block")

            # Если в инвентаре есть золотой меч
            # И курсор находится на его позиции
            if self.inventory.inv[0][i] == "gold_sword":
                if self.current_cursor_pos == i:
                    # Установка блока в зависимости
                    # От положения игрока
                    if self.player.mirrored:
                        if self.world.entities[y][xr] < 5:
                            self.world.entities[y][xr] = 6
                            self.world.render()
                            entities_group.update()
                            self.put_block("gold_sword")
                    else:
                        if self.world.entities[y][xl] < 5:
                            self.world.entities[y][xl] = 6
                            self.world.render()
                            entities_group.update()
                            self.put_block("gold_sword")

            # Если в инвентаре есть серебрянный меч
            # И курсор находится на его позиции
            if self.inventory.inv[0][i] == "silver_sword":
                if self.current_cursor_pos == i:
                    # Установка блока в зависимости
                    # От положения игрока
                    if self.player.mirrored:
                        if self.world.entities[y][xr] < 5:
                            self.world.entities[y][xr] = 7
                            self.world.render()
                            entities_group.update()
                            self.put_block("silver_sword")
                    else:
                        if self.world.entities[y][xl] < 5:
                            self.world.entities[y][xl] = 7
                            self.world.render()
                            entities_group.update()
                            self.put_block("silver_sword")

    def destroy_object(self, x, y, xl, xr, yu, yd):
        ifdestroy = False  # Флаг разрушенности блоков
        # Слева, если это природные объекты
        if 0 < self.world.entities[y][xl] < 5:
            self.world.entities[y][xl] = 0
            self.append_drop(xl, y)
            ifdestroy = True

        # Слева, если это мясной блок
        if self.world.entities[y][xl] == 5:
            self.world.entities[y][xl] = 0
            self.append_drop_block(xl, y, 5)
            ifdestroy = True

        # Слева, если это золотой меч
        if self.world.entities[y][xl] == 6:
            self.world.entities[y][xl] = 0
            self.append_drop_block(xl, y, 6)
            ifdestroy = True

        # Слева, если это серебрянный меч
        if self.world.entities[y][xl] == 7:
            self.world.entities[y][xl] = 0
            self.append_drop_block(xl, y, 7)
            ifdestroy = True

        # Вправо, если это природные объекты
        if 0 < self.world.entities[y][xr] < 5:
            self.world.entities[y][xr] = 0
            self.append_drop(xr, y)
            ifdestroy = True

        # Вправо, если это мясной блок
        if self.world.entities[y][xr] == 5:
            self.world.entities[y][xr] = 0
            self.append_drop_block(xr, y, 5)
            ifdestroy = True

        # Вправо, если это золотой меч
        if self.world.entities[y][xr] == 6:
            self.world.entities[y][xr] = 0
            self.append_drop_block(xr, y, 6)
            ifdestroy = True

        # Вправо, если это серебрянный меч
        if self.world.entities[y][xr] == 7:
            self.world.entities[y][xr] = 0
            self.append_drop_block(xr, y, 7)
            ifdestroy = True

        # Снизу, если это природные объекты
        if 0 < self.world.entities[yd][x] < 5:
            self.world.entities[yd][x] = 0
            self.append_drop(x, yd)
            ifdestroy = True
        # Снизу, если это мясной блок
        if self.world.entities[yd][x] == 5:
            self.world.entities[yd][x] = 0
            self.append_drop_block(x, yd, 5)
            ifdestroy = True

        # Снизу, если это золотой меч
        if self.world.entities[yd][x] == 6:
            self.world.entities[yd][x] = 0
            self.append_drop_block(x, yd, 6)
            ifdestroy = True

        # Снизу, если это серебрянный меч
        if self.world.entities[yd][x] == 7:
            self.world.entities[yd][x] = 0
            self.append_drop_block(x, yd, 7)
            ifdestroy = True

        # Сверху, если это природные объекты
        if 0 < self.world.entities[yu][x] < 5:
            self.world.entities[yu][x] = 0
            self.append_drop(x, yu)
            ifdestroy = True

        # Сверху, если это мясной блок
        if self.world.entities[yu][x] == 5:
            self.world.entities[yu][x] = 0
            self.append_drop_block(x, yu, 5)
            ifdestroy = True

        # Сверху, если это золотой меч
        if self.world.entities[yu][x] == 6:
            self.world.entities[yu][x] = 0
            self.append_drop_block(x, yu, 6)
            ifdestroy = True

        # Сверху, если это серебрянный меч
        if self.world.entities[yu][x] == 7:
            self.world.entities[yu][x] = 0
            self.append_drop_block(x, yu, 7)
            ifdestroy = True

        # По центру, если это природные объекты
        if 0 < self.world.entities[y][x] < 5:
            self.world.entities[y][x] = 0
            self.append_drop(x, y)
            ifdestroy = True

        # По центру, если это мясной блок
        if self.world.entities[y][x] == 5:
            self.world.entities[y][x] = 0
            self.append_drop_block(x, y, 5)
            ifdestroy = True

        # По центру, если это золотой меч
        if self.world.entities[y][x] == 6:
            self.world.entities[y][x] = 0
            self.append_drop_block(x, y, 6)
            ifdestroy = True

        # По центру, если это серебрянный меч
        if self.world.entities[y][x] == 7:
            self.world.entities[y][x] = 0
            self.append_drop_block(x, y, 7)
            ifdestroy = True

        # Само уничтожение
        if ifdestroy:
            # Обновление групп спрайтов и мира
            self.world.render()
            entities_destroy.play()
            entities_group.update()
            drop_group.update()

    def run(self):
        enable_sfx()  # Проверка Вкл/Выкл звуковых эффектов
        # Загружаю мир и инвентарь
        self.world.render()
        self.inventory.render()

        # Обновляю группы спрайтов
        tiles_group.update()
        all_sprites.update()
        animal_group.update()
        inventory_group.update()
        entities_group.update()
        drop_group.update()

        # Кнопки паузы
        continue_txt = start_menu_text.render("Continue", 0, (100, 100, 100))
        continue_rect = continue_txt.get_rect().move(60, 100)

        quit_txt = start_menu_text.render("Quit", 0, (100, 100, 100))
        quit_rect = quit_txt.get_rect().move(60, 160)
        while self.running:
            # Положение игрока внутри матрицы мира
            x = int((self.player.rect.x + 32) / 4096 * 64)
            y = int((self.player.rect.y + 32) / 4096 * 64)
            xl = x - 1  # Клетка слева
            xr = x + 1  # Клетка справа
            yu = y - 1  # Клетка сверху
            yd = y + 1  # Клетка снизу
            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Если пауза не активирована
            if not self.pause:
                pg.mouse.set_visible(False)  # Скрыть курсор
                self.dt = self.clock.tick(self.FPS) / 1000
                # Время в игре
                self.time_in_game += self.dt
                # Функция пожирания мира
                self.world_cutting()
                # Обновлять положение камеры за игроком
                self.camera.update(self.player)
                # Обновлять игровой мир
                self.update_tiles()

                # Проверка кравта и его отображение
                self.craft.craft_type = -1
                self.craft_checking()
                self.craft.render()
                # Обновлене частиц
                particle_group.update()

            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False

                if event.type == pg.MOUSEMOTION:
                    # Анимация текста при включенной паузе
                    if self.pause:
                        if continue_rect.collidepoint(event.pos):
                            continue_txt = start_menu_text.render(
                                "Continue", 0, (255, 255, 255))
                        else:
                            continue_txt = start_menu_text.render(
                                "Continue", 0, (100, 100, 100))

                        if quit_rect.collidepoint(event.pos):
                            quit_txt = start_menu_text.render(
                                "Quit", 0, (255, 255, 255))
                        else:
                            quit_txt = start_menu_text.render(
                                "Quit", 0, (100, 100, 100))

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.pause:
                            # Кнопка продолжить игру
                            if continue_rect.collidepoint(event.pos):
                                self.pause = False
                            # Кнопка выхода из игры
                            if quit_rect.collidepoint(event.pos):
                                self.running = False

                if event.type == pg.KEYDOWN:
                    # Очистка дропа, если касается игрок.
                    self.drop_clean()

                    if not self.pause:  # Пока не пауза
                        # Открытие меню паузы
                        if event.key == pg.K_ESCAPE:
                            self.pause = True

                        #  Уничтожение блоков
                        if event.key == pg.K_SPACE:
                            self.destroy_object(x, y, xl, xr, yu, yd)

                        # Установка блоков
                        if event.key == pg.K_m:
                            self.create_object(y, xl, xr)

                        # Смена инструмента
                        if event.key == pg.K_o:
                            # Если был топор, станут ножницы
                            if self.tool == "axe":
                                self.tool = "scissors"
                            # И наоборот
                            else:
                                self.tool = "axe"

                        # Убийство коровы aka "Быстрое убийство"
                        if event.key == pg.K_k:
                            self.cow_and_player()

                        # Создание вещей
                        if event.key == pg.K_c:
                            b = 0  # Подсчет компонентов
                            # Индексы ячеек элементов создания вещей
                            index1 = 0
                            index2 = 0
                            # Создание сухожилий
                            if self.craft.craft_type == 0:
                                for i in range(self.inventory.w):
                                    # Если мяса и сухожилий больше
                                    # или равно одной штуке в инвентаре
                                    if self.inventory.inv[0][i] == "meat"\
                                            and self.inventory.inv[1][i] > 0:
                                        b += 1
                                        index1 = i
                                    if self.inventory.inv[0][i] == "eyes"\
                                            and self.inventory.inv[1][i] > 0:
                                        b += 1
                                        index2 = i
                                # Если это так, то идет создание сухожилий
                                if b == 2:
                                    # Отнимаются соотвественно вещи
                                    self.inventory.inv[1][index1] -= 1
                                    self.inventory.inv[1][index2] -= 1
                                    if self.inventory.inv[1][index1] == 0:
                                        self.inventory.invtmp.remove(
                                            self.inventory.inv[0][index1])
                                        self.inventory.inv[0][index1] = 0

                                    if self.inventory.inv[1][index2] == 0:
                                        self.inventory.invtmp.remove(
                                            self.inventory.inv[0][index2])
                                        self.inventory.inv[0][index2] = 0
                                    # Сухожилие добавлено в инвентарь
                                    self.inventory.append("meat_block")

                            if self.craft.craft_type == 1:
                                for i in range(self.inventory.w):
                                    # Если золота в инвентаре больше
                                    # одной штуки, то идет создание меча
                                    if self.inventory.inv[0][i] == "gold"\
                                            and self.inventory.inv[1][i] > 1:
                                        b += 1
                                        index1 = i
                                # Если это так, то идет создание золотого меча
                                if b:
                                    # Отнимаются соотвественно вещи
                                    self.inventory.inv[1][index1] -= 2
                                    if self.inventory.inv[1][index1] == 0:
                                        self.inventory.invtmp.remove(
                                            self.inventory.inv[0][index1])
                                        self.inventory.inv[0][index1] = 0
                                    # Золотой меч добавлен в инвентарь
                                    self.inventory.append("gold_sword")

                        # Изменение положения курсора в инвентаре
                        if event.key == pg.K_p:
                            # Если курсор еще не в конце инветаря
                            if self.current_cursor_pos < self.inventory.w - 1:
                                self.current_cursor_pos += 1
                            # Если курсор уже на последней ячейке,
                            # то он переходит на первую
                            else:
                                self.current_cursor_pos = 0  # Сброс курсора

            if self.pause:
                # Когда пауза, курсор и кнопки:
                # Продолжить, Выйти - активированы
                pg.mouse.set_visible(True)
                # Добавление кнопок меню паузы на экран
                screen.blit(continue_txt, (60, 100))  # Продолжить
                screen.blit(quit_txt, (60, 160))  # Выйти

            if not self.pause:
                # Если весь мир сожран, то игра завершается с проигрышем
                if self.step == 33:
                    GameOver().run()

                # Проверка положения коров
                self.check_cows()

                # Проверка выигрыша или активации секретного уровня
                for j in range(self.world.w):
                    for i in range(self.world.w):
                        if j != 63 and i != 63:
                            '''
                            Если тотем построен в виде:
                            С С С
                            С М С - где М - Золотой меч,
                            С С С       С - Сухожилие,
                            то игра завершается и игрок выигрывает
                            '''
                            if self.world.entities[j][i] == 5 and \
                                self.world.entities[j][i + 1] == 5 and \
                                self.world.entities[j][i + 2] == 5 and \
                                self.world.entities[j + 1][i] == 5 and \
                                self.world.entities[j + 1][i + 1] == 6 and \
                                self.world.entities[j + 1][i + 2] == 5 and \
                                self.world.entities[j + 2][i] == 5 and\
                                self.world.entities[j + 2][i + 1] == 5 and\
                                    self.world.entities[j + 2][i + 2] == 5:
                                Win(str(datetime.timedelta(
                                    seconds=int(self.time_in_game))),
                                    self.difficult).run()
                            '''
                            Если тотем построен в виде:
                            С С С
                            С S С - где S - Серебрянный меч,
                            С С С       С - Сухожилие,
                            то игра завершается и секретный уровень активирован
                            '''
                            if self.world.entities[j][i] == 5 and \
                                self.world.entities[j][i + 1] == 5 and \
                                self.world.entities[j][i + 2] == 5 and \
                                self.world.entities[j + 1][i] == 5 and \
                                self.world.entities[j + 1][i + 1] == 7 and \
                                self.world.entities[j + 1][i + 2] == 5 and \
                                self.world.entities[j + 2][i] == 5 and \
                                self.world.entities[j + 2][i + 1] == 5 and\
                                    self.world.entities[j + 2][i + 2] == 5:
                                global psycho_level
                                psycho_level = 1
                                GameOver().run()

                # Обновить игрока и животных
                animal_group.update()
                all_sprites.update()

                # Обновить инвентарь
                self.inventory.render()
                inventory_group.update()
                inventory_group.draw(screen)

                # Текущий инструмент в руках героя
                axe_scissors = load_image(str(self.tool) + ".png")
                axe_scissors = pg.transform.scale(axe_scissors, (72, 72))
                # Добавление текущего инструмента в руках героя на экран
                screen.blit(start_menu_text.render(
                    str(self.tool), 0, (255, 255, 255)), (64, 72))
                screen.blit(axe_scissors, (64, 0))
                screen.blit(self.cursor,
                            (72 * self.current_cursor_pos + 240, 0))
            # Обновление кадра
            pg.display.flip()
        # Запуск меню
        open_menu()


# Игровой мир (Карта)
class TileMap:
    def __init__(self):
        self.w = 66  # Длина мира
        self.h = 66  # Ширина мира
        # Карта поверхностей
        self.world_array = [[0] * self.w for _ in range(self.h)]
        # Карта природных объектов
        self.entities = [[0] * self.w for _ in range(self.h)]
        self.generation()  # Генерация мира
        self.cell_size = 64  # Размер клетки мира
        '''
        self.entities_enabled - флаг, отвечающий на единственную
        генерацию природных объектов.
        '''
        self.entities_enabled = False

    # Генерация мира
    def generation(self):
        for j in range(self.h):
            for i in range(self.w):
                b = random.randint(0, 100)
                '''
                Генерация происходит по принципу
                65% == Трава, Земля == 0
                15% == Песок == 1
                20% == Камень == 2
                '''
                if b < 65:
                    self.world_array[j][i] = 0
                elif 65 <= b < 80:
                    self.world_array[j][i] = 1
                else:
                    self.world_array[j][i] = 2
        # Начертание границ по длине
        for i in range(self.w):
            self.world_array[0][i] = -1
            self.world_array[-1][i] = -1

        # Начертание границ по ширине
        for i in range(self.h):
            self.world_array[i][0] = -1
            self.world_array[i][-1] = -1

    def render(self):
        # Очистка групп спрайтов для разгрузки памяти
        tiles_group.empty()
        entities_group.empty()
        # Заполнение спрайтами мира
        for i in range(self.w):
            for j in range(self.h):
                # Границы мира
                if self.world_array[j][i] == -1:
                    Tile('empty', i, j)
                    # Природные объекты за границами - уничтожаются
                    if self.entities[j][i] != 0:
                        self.entities[j][i] = 0

                # Трава
                if self.world_array[j][i] == 0:
                    Tile('grass', i, j)
                    if not self.entities_enabled:
                        entity = random.randint(0, 100)
                        if entity < 40:
                            self.entities[j][i] = 1
                        elif 45 > entity >= 40:
                            self.entities[j][i] = 2
                        elif 60 > entity >= 50:
                            self.entities[j][i] = 3
                # Песок
                if self.world_array[j][i] == 1:
                    Tile('sand', i, j)
                    if not self.entities_enabled:
                        entity = random.randint(0, 100)
                        if entity < 4:
                            self.entities[j][i] = 4
                # Камень
                if self.world_array[j][i] == 2:
                    Tile('stone', i, j)
                    if not self.entities_enabled:
                        entity = random.randint(0, 100)
                        if entity < 11:
                            self.entities[j][i] = 4
                '''
                Если генерация мира не произведена
                то природные объекты генерируются
                по приницпу:
                60% == Трава
                20% == Песок
                20% == Камень
                '''
                if self.entities[j][i] == -2:
                    Entity('blood', i, j)
                # Трава
                if self.entities[j][i] == 1:
                    Entity('green', i, j)
                # Цветы
                if self.entities[j][i] == 2:
                    Entity('flowers', i, j)
                # Кусты
                if self.entities[j][i] == 3:
                    Entity('bush', i, j)
                # Камень
                if self.entities[j][i] == 4:
                    Entity('rock', i, j)
                # Мясо
                if self.entities[j][i] == 5:
                    Entity('meat', i, j)
                # Золотой меч
                if self.entities[j][i] == 6:
                    Entity('gold_sword', i, j)
                # Серебрянный меч
                if self.entities[j][i] == 7:
                    Entity('silver_sword', i, j)
        # После первой генерации мира, больше нет права генерировать
        self.entities_enabled = True


# Камера
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        # Маска камеры прямоугольником
        self.camera = pg.Rect(0, 0, 4224, 4224)

        self.width = 4224   # Размер всей карты по длине
        self.height = 4224  # Размер всей карты по ширине

    # сдвинуть спрайты на смещение камеры
    def apply(self, obj):
        return obj.rect.move(self.camera.topleft)

    def update(self, target):
        # Положение камеры берет разность середины экрана
        # и положения игрока вместе с его размерами
        x = -target.rect.x - target.rect.w + int(640 // 2)
        y = -target.rect.y - target.rect.h + int(512 // 2)

        '''
        Ограничения(экстремумы) координат, нужны для того
        чтобы, когда игрок за пределами середины, он мог
        cвободно перемещатся, без смещения остальных
        cпрайтов.
        '''

        x = min(0, x)  # ограничение на левый край
        y = min(0, y)  # ограничение на верхний край
        x = max(-(self.width - 640), x)  # на правый край
        y = max(-(self.height - 512), y)  # на нижний

        # Камера получает новую маску
        self.camera = pg.Rect(x, y, self.width, self.height)


# Ячейка спрайта игрового поля
class Tile(pg.sprite.Sprite):
    def __init__(self, types, x, y):
        super().__init__(tiles_group)
        self.cell_size = 64  # Размер ячейки
        self.type = types  # Тип ячейки, для загрузки соответсвующего спрайта
        self.image = tile_images[types]  # Загрузка спрайта
        # Изменение размеров ячейки
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))
        # Прямоугольная маска
        self.rect = self.image.get_rect().move(self.cell_size * x,
                                               self.cell_size * y)


# Природные объекты
class Entity(pg.sprite.Sprite):
    def __init__(self, types, x, y):
        super().__init__(entities_group)
        self.cell_size = 64  # Размер клетки
        self.image = entity_images[types]   # Спрайт из словаря
        # Изменение размеров изображения
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))
        # Маска спрайта из прямоугольника
        self.rect = self.image.get_rect().move(self.cell_size * x,
                                               self.cell_size * y)

    # Уничтожение клетки, если что-то поставили
    def get_out(self, tile):
        if self.rect.collidepoint(tile.rect.topleft):
            self.kill()


# Игрок
class Player(pg.sprite.Sprite):
    def __init__(self, group, game, x, y, cell_size, gender):
        super().__init__(group)
        self.game = game    # Параметр текущей игра
        self.state = "stay"  # Изначально положение героя
        self.frames = []    # Лист кадров
        self.cur_frame = 0  # Текущий кадр
        self.mirrored = False   # Параметр отзеркаливания героя
        self.gender = gender    # Параметр пола персонажа

        # Если выбрали Мартина, то соответсвующий спрайт
        if self.gender == "male":
            self.cut_sheet(load_image("p_sheet.png"))
        # Если выбрали Марго, то соответствующий спрайт
        else:
            self.cut_sheet(load_image("f_sheet.png"))

        # Картинка береться из листа
        self.image = self.frames[self.cur_frame]

        # Параметр размера спрайта
        self.size = self.image.get_size()

        # Маска спрайта из прямоугольника
        self.rect = self.image.get_rect()
        self.cell_size = cell_size

        # Скорость героя
        self.speed = 150

        self.vx = 0  # Скорость героя на проекцию Ox
        self.vy = 0  # Скорость героя на проекцию Oy

        self.timer = 0  # Таймер смены кадров анимации
        self.timer_animation = 0  # Таймер смены анимации
        self.x = x * cell_size  # Координаты героя на ось Ox
        self.y = y * cell_size  # Координаты героя на ось Oy

    def cut_sheet(self, sheet):
        self.frames.clear()  # Очистить лист для перезагрузки кадров
        self.rect = pg.Rect(0, 0, sheet.get_width() // 6,
                            sheet.get_height() // 2)
        # Если состояние бега, то отрезаются спрайты бега
        if self.state == "run":
            for j in range(1, 2):
                for i in range(6):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pg.Rect(
                        frame_location, self.rect.size)))

            self.frames = self.frames[0:6]  # Отрезать 6 спрайтов бега
        # Если состояние стойки, то отрезаются спрайты стойки
        if self.state == "stay":
            for j in range(0, 1):
                for i in range(2):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pg.Rect(
                        frame_location, self.rect.size)))

            self.frames = self.frames[0:2]  # Отрезать 2 спрайта бега

    def key_movement(self):
        self.vx = 0  # Сброс скорости на проекцию Ox
        self.vy = 0  # Сброс скорости на проекцию Oy
        keys = pg.key.get_pressed()  # Отслеживать зажатые клавиши
        self.timer_animation += self.game.dt  # Таймер между кадрами анимациями

        # Если игрок не заходит за границы Oy
        if self.y > self.game.step * 64:
            if keys[pg.K_w]:    # Управление вверх
                self.vy = -self.speed
                # Смена кадра через 0.08 секунд
                if self.timer_animation > 0.08:
                    self.game.player_run()  # Запуск анимации бега
                    self.timer_animation = 0  # Сброс таймера

        else:  # Если игрок за границами Oy
            self.vy += 72  # Плавно отодвинуть игрока

        # Если игрок не заходит за границы Oy
        if self.y < (65 - self.game.step) * 64:
            if keys[pg.K_s]:  # Управление вниз
                self.vy = self.speed
                # Смена кадра через 0.08 секунд
                if self.timer_animation > 0.08:
                    self.game.player_run()  # Запуск анимации бега
                    self.timer_animation = 0  # Сброс таймера

        else:  # Если игрок за границами Oy
            self.vy -= 72  # Плавно отодвинуть игрока

        # Если игрок не заходит за границы Ox
        if self.x > self.game.step * 64:
            if keys[pg.K_a]:  # Управление влево
                self.vx = -self.speed
                self.mirrored = False  # Игрок смотрит налево
                # Смена кадра через 0.08 секунд
                if self.timer_animation > 0.08:
                    self.game.player_run()  # Запуск анимации бега
                    self.timer_animation = 0  # Сброс таймера

        else:  # Если игрок за границами Ox
            self.vx += 72  # Плавно отодвинуть игрока

        # Если игрок не заходит за границы Ox
        if self.x < (65 - self.game.step) * 64:
            if keys[pg.K_d]:  # Управление вправо
                self.vx = self.speed
                self.mirrored = True  # Игрок смотрит направо
                # Смена кадра через 0.08 секунд
                if self.timer_animation > 0.08:
                    self.game.player_run()  # Запуск анимации бега
                    self.timer_animation = 0  # Сброс таймера

        else:  # Если игрок за границами Ox
            self.vx -= 72  # Плавно отодвинуть игрока

        # Если игрок не двигается, идет состояние и анимация стойки
        if self.vx == 0 and self.vy == 0:
            self.state = "stay"
            # Смена кадра через 0.15 секунд
            if self.timer_animation > 0.15:
                self.game.player_stay()  # Запуск анимации стойки
                self.timer_animation = 0  # Сброс таймера

        # Если игрок в движении, идет состояние бега
        else:
            self.state = "run"

    def update(self):
        self.timer += self.game.dt  # Таймер смены кадров
        # Смена кадров при беге 0.05 секунд
        if self.state == "run":
            if self.timer > 0.05:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.timer = 0  # Сброс таймера

        # Смена кадров при стойки 0.5 секунд
        if self.state == "stay":
            if self.timer > 0.5:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.timer = 0  # Сброс таймера

        # Изменять размер спрайта
        self.image = pg.transform.scale(self.image,
                                        (int(self.size[0] * 4),
                                         int(self.size[1] * 4)))
        # Проверять управление игрока
        self.key_movement()
        # Передвижение игрока
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y


# Инвентарь
class Inventory:
    def __init__(self):
        self.w = 5  # Длина инветаря
        self.inv = [[0] * self.w for _ in range(2)]  # Лист инвентаря
        self.invtmp = []    # Буферный лист инвентаря

    def render(self):
        inventory_group.empty()  # Очистить все спрайты инветаря
        for i in range(self.w):
            # Пустой слот
            if self.inv[0][i] == 0 or self.inv[1][i] == 0:
                InventoryTile('empty', i)
            # Слот с золотом
            if self.inv[0][i] == "gold" and self.inv[1][i] != 0:
                InventoryTile('gold', i)
            # Слот с серебрянным мечом
            if self.inv[0][i] == "silver_sword" and self.inv[1][i] != 0:
                InventoryTile('silver_sword', i)
            # Слот с золотым мечом
            if self.inv[0][i] == "gold_sword" and self.inv[1][i] != 0:
                InventoryTile('gold_sword', i)
            # Слот с мясом
            if self.inv[0][i] == "meat" and self.inv[1][i] != 0:
                InventoryTile('meat', i)
            # Слот с глазами
            if self.inv[0][i] == "eyes" and self.inv[1][i] != 0:
                InventoryTile('eyes', i)
            # Слот с сухожилием
            if self.inv[0][i] == "meat_block" and self.inv[1][i] != 0:
                InventoryTile('meat_block', i)
            # Слот с жертвами
            if self.inv[0][i] == "victim1" and self.inv[1][i] != 0:
                InventoryTile('victim1', i)
            if self.inv[0][i] == "victim2" and self.inv[1][i] != 0:
                InventoryTile('victim2', i)
            if self.inv[0][i] == "victim3" and self.inv[1][i] != 0:
                InventoryTile('victim3', i)
            if self.inv[0][i] == "victim4" and self.inv[1][i] != 0:
                InventoryTile('victim4', i)
            if self.inv[0][i] == "victim5" and self.inv[1][i] != 0:
                InventoryTile('victim5', i)
            # Добавление ячеек инвентаря на экран
            screen.blit(start_menu_text.render(str(self.inv[1][i]),
                                               0, (255, 255, 255)),
                        (284 + (i * 72), 72))

    def append(self, type_obj):
        # Добавление вещей в инвентарь
        for i in range(self.w):
            # Если такого предмета нет в инвентаре, он попадает в новый слот
            if type_obj not in self.invtmp:
                if self.inv[0][i] == 0:
                    self.inv[0][i] = type_obj
                    self.inv[1][i] += 1
                    self.invtmp.append(type_obj)
            # Если такой предмет существует в инвентаре, он прибавляется
            else:
                if self.inv[0][i] == type_obj:
                    self.inv[0][i] = type_obj
                    self.inv[1][i] += 1

    def check_craft_meat(self):
        b = 0
        # Проверка предметов для соотвествующего кравта(мяса)
        for i in range(self.w):
            if self.inv[0][i] == "meat" and self.inv[1][i] >= 1:
                b += 1
            if self.inv[0][i] == "eyes" and self.inv[1][i] >= 1:
                b += 1
        if b == 2:
            return True
        else:
            return False

    def check_craft_gold(self):
        b = 0
        # Проверка предметов для соотвествующего кравта(золотой меч)
        for i in range(self.w):
            if self.inv[0][i] == "gold" and self.inv[1][i] == 2:
                b += 1
        return b


# Создание вещей
class Craft:
    def __init__(self):
        # Создание мяса
        self.craft_meat = load_image("craft_meat.png")
        self.craft_meat = pg.transform.scale(self.craft_meat, (360, 72))

        # Создание золота
        self.craft_gold = load_image("craft_gold.png")
        self.craft_gold = pg.transform.scale(self.craft_gold, (360, 72))
        self.craft_type = -1    # Текущий кравт обнулен

    def render(self):
        if self.craft_type == 0:
            # Добавить объект кравта мяса на экран
            screen.blit(self.craft_meat, (150, 440))

        if self.craft_type == 1:
            # Добавить объект кравта золота на экран
            screen.blit(self.craft_gold, (150, 440))


# Ячейка инвентаря
class InventoryTile(pg.sprite.Sprite):
    def __init__(self, types, x):
        super().__init__(inventory_group)
        self.cell_size = 72  # Размер ячейки
        self.image = inventory_images[types]    # Спрайт из словаря
        # Изменяются размеры спрайта ячейки
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))
        # Прямоугольная маска спрайта
        self.rect = self.image.get_rect().move(self.cell_size * x + 240, 0)


# Выпадение вещей
class Drop(pg.sprite.Sprite):
    def __init__(self, types, player, x, y, game):
        super().__init__(drop_group)
        self.type = types   # Тип вещи
        self.cell_size = 64  # Размер клетки
        self.image = drop_images[types]  # Спрайт берется из словаря
        # Изменяются размеры
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))
        # Прямоугольная маска спрайта
        self.rect = self.image.get_rect().move(self.cell_size * x,
                                               self.cell_size * y)
        self.player = player    # Текущий игрок
        self.step = game.step   # Текущее состояние пожирания мира

    def get_event(self):
        # Если игрок касается выпавшей вещи
        if self.rect.collidepoint((self.player.rect.x + 32),
                                  (self.player.rect.y + 32)):
            pick_up_sound.play()
            return True

    def check_drop_pos(self):
        # Вещи уничтожаются при соприкосновении с границей мира
        if self.rect.x < 64 * self.step:
            return 1

        if self.rect.x > 64 * (65 - self.step):
            return 1

        if self.rect.y < 64 * self.step:
            return 1

        if self.rect.y > 64 * (65 - self.step):
            return 1


# Частицы крови
class Blood(pg.sprite.Sprite):
    fire = [load_image("blood.png")]
    for scale in (5, 10, 20):
        fire.append(pg.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particle_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


# Моя учительница по истории
class Cow(pg.sprite.Sprite):
    def __init__(self, group, game, x, y, cell_size):
        super().__init__(group)
        self.game = game    # привязанный параметр текущей игры
        self.state = "stay"  # текущее положение, для анимации
        self.tmpstate = False  # буферное положение, для переключения анимации
        self.type_obj = random.randint(0, 1)
        self.frames = []    # Лист кадров
        self.cur_frame = 0  # Текущий кадр
        self.mirrored = False  # Отразить коровку
        # Полотно спрайтов коровки
        self.cut_sheet(load_image("c" + str(self.type_obj) + "_sheet.png"))

        self.image = self.frames[self.cur_frame]    # Картинка из листа
        self.size = self.image.get_size()   # Получить размер картинки

        self.rect = self.image.get_rect()   # Получить маску из прямоугольника
        self.cell_size = cell_size  # Текущий размер клетки в игровом мире

        self.speed = 100    # Скорость коровки

        self.vx = 0  # Скорость коровки на проекцию Ox
        self.vy = 0  # Скорость коровки на проекцию Oy

        self.timer = 0  # Таймер переключения анимаций
        self.timer_choose_animation = 0  # Таймер свободного движения коровки
        self.timer_run = 0

        self.x = x * cell_size  # Изначальное положение коровки на ось Ox
        self.y = y * cell_size  # Изначальное положение коровки на ось Oy

        self.movement(random.randint(0, 4))  # Случайный выбор движения

        self.hp = 10    # Жизнь коровки

    def check_hp(self):
        if self.hp < 1:  # Если коровка уже не в Индии
            return 1  # То минус коровка(когда у коровки 0 жизней)

    def comparestates(self):    # Сравнение анимаций
        if self.tmpstate != self.state:
            self.frames.clear()  # Очистка листа спрайтов
            self.tmpstate = self.state  # Буферное приравнивается к текущему

    def cut_sheet(self, sheet):
        self.comparestates()    # Вызвать функцию состояний анимации
        self.frames.clear()  # Чтобы удалить остаточные кадры
        # Получить маску прямоугольника из картинки
        self.rect = pg.Rect(0, 0, sheet.get_width() // 2,
                            sheet.get_height() // 2)

        if self.state == "run":  # Если текущее состояние коровки == бег
            for j in range(1, 2):
                for i in range(2):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(
                        pg.Rect(frame_location, self.rect.size)))

        if self.state == "stay":  # Если текущее состояние коровки == стоять
            for j in range(0, 1):
                for i in range(2):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(
                        pg.Rect(frame_location, self.rect.size)))
        # Оставлять в листе только 2 спрайта(т.к. в полотне было 2 ячейки)
        self.frames = self.frames[0:2]

    def movement(self, b):
        self.vx = 0  # Скорость коровки на проекцию Ox
        self.vy = 0  # Скорость коровки на проекцию Oy

        # Если коровка стоит
        if b == 0:
            self.vx = 0
            self.vy = 0
            self.state = "stay"
            if self.mirrored:
                self.cut_sheet(load_image("cm" + str(self.type_obj) + "_sheet.png"))
            else:
                self.cut_sheet(load_image("c" + str(self.type_obj) + "_sheet.png"))

        # Если коровка идет налево
        if b == 1:
            self.vx = -self.speed
            self.mirrored = False

        # Если коровка идет направо
        if b == 2:
            self.vx = self.speed
            self.mirrored = True

        # Если коровка идет вверх
        if b == 3:
            self.vy = -self.speed

        # Если коровка идет вниз
        if b == 4:
            self.vy = self.speed

        # Если коровка не стоит, то проигрывается анимация бега
        if b > 0:
            self.state = "run"
            # Чтобы коровка могла смотреть по сторонам(отражение)
            if self.mirrored:
                self.cut_sheet(load_image("cm" + str(self.type_obj) + "_sheet.png"))
            else:
                self.cut_sheet(load_image("c" + str(self.type_obj) + "_sheet.png"))

    def update(self):
        # Таймер побега от игрока
        if self.timer_run > 0:
            self.timer_run -= self.game.dt
            self.speed = 200
        else:
            self.speed = 100
        # Интервал между кадрами
        self.timer += self.game.dt
        # Интервал изменения направления
        self.timer_choose_animation += self.game.dt

        # Если текущее состояние == стоять, то интервал = 1 секунды
        if self.state == "stay":
            if self.timer > 1:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.timer = 0

        # Если текущее состояние == бег, то интервал = 0.3 секунды
        if self.state == "run":
            if self.timer > 0.3:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.timer = 0

        # Изменение размеров картинки
        self.image = pg.transform.scale(self.image,
                                        (int(self.size[0] * 4),
                                         int(self.size[1] * 4)))

        # Каждые 2 секунды коровка будет двигатся по-разному
        if self.timer_choose_animation > 2:
            self.timer_choose_animation = 0
            self.movement(random.randint(0, 4))

        # Двигать коровку под FPS
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y


# Секретный уровень
class SecretLevel:
    def __init__(self):
        clear_tiles()
        self.running = True
        self.step = 0  # За пределы карты, игрок не сможет выйти
        self.dt = 0  # Обновление времени внутри системы
        self.FPS = 100  # Кадры в секунду для оптимизации
        self.clock = pg.time.Clock()  # Внутриигровые часы
        self.children = 5  # Подсчет оставшихся полотенец(внутри дети)
        self.drop = []  # Лист собравшихся полотенец
        self.player = Player(all_sprites,
                             self, 30, 31, 64, "female")  # Текущий игрок
        self.inventory = Inventory()  # Текущий инвентарь
        self.camera = Camera()  # Текущая камера
        # К каждому полотенцу будет взято рандомные числа X, Y - его координаты
        # random.sample -  делает так, чтобы координаты не повторялись
        self.list_coordinates_victims = random.sample(range(1, 63), 10)
        self.screamer = 0  # Индикатор скримера
        self.tmplist = []  # Буферный лист полотенец
        # Скример
        self.screamer_img = load_image("screamer.png")
        # Затемненные края
        self.overlay = load_image("overlay.png")

    def update_tiles(self):
        # Передвижение всех спрайтов вдоль камеры
        for sprite in secret_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))

    def player_run(self):
        # Обработка бегающего игрока
        self.player.state = "run"
        self.player.timer = 0.05
        self.gender()

    def gender(self):
        if self.player.mirrored:
            self.player.cut_sheet(load_image("fm_sheet.png"))
        else:
            self.player.cut_sheet(load_image("f_sheet.png"))

    def player_stay(self):
        # Обработка стоячего игрока
        self.player.state = "stay"
        self.player.timer = 0.5
        self.gender()

    def check_victims(self):
        # Проверка упавших полотенец и добавление их в инвентарь
        # Если игрок касается полотенца, оно уничтожается,
        # а игрок получает в инвентарь соотвествующее полотенце
        if self.drop:
            for i in range(len(self.drop)):
                self.drop[i].kill()
                self.inventory.append(self.drop[i].type)
                self.tmplist.append(i)
        # Если буферный лист забит, то он очищает лист упавших полотенец,
        #  в целях того, чтобы не добавлялось 1+ полотенец, а только одно
        if self.tmplist:
            for i in range(len(self.tmplist)):
                self.children -= 1
                self.list_victims.remove(self.drop[i])
                del self.drop[self.tmplist[i]]

    def run(self):
        enable_sfx()  # Проверка Вкл/Выкл звуковых эффектов
        inventory_group.empty()
        # Загружаю мир и инвентарь
        SecretTile('bath', 30, 30, self.player)
        SecretTile('shower', 31, 30, self.player)
        SecretTile('left_eye', 29.5, 29, self.player)
        SecretTile('right_eye', 30.5, 29, self.player)
        # Загружаю полотенца
        self.list_victims = [SecretTile(
            'victim1', self.list_coordinates_victims[0],
            self.list_coordinates_victims[1], self.player),
                             SecretTile(
            'victim2', self.list_coordinates_victims[2],
            self.list_coordinates_victims[3], self.player),
                             SecretTile(
            'victim3', self.list_coordinates_victims[4],
            self.list_coordinates_victims[5], self.player),
                             SecretTile(
            'victim4', self.list_coordinates_victims[6],
            self.list_coordinates_victims[7], self.player),
                             SecretTile(
            'victim5', self.list_coordinates_victims[8],
            self.list_coordinates_victims[9], self.player)]
        # Перезагружаю инвентарь
        self.inventory.render()

        # Обновляю группы спрайтов
        all_sprites.update()
        inventory_group.update()
        drop_group.update()

        # Лист, чтобы прослеживать уже добавленные предметы
        self.tmplist = []
        while self.running:
            # Обновление экрана путем заливки
            screen.fill((0, 0, 0))
            pg.mouse.set_visible(False)  # Отключить курсор
            self.dt = self.clock.tick(self.FPS) / 1000
            # Обновлять камеру за игроком
            self.camera.update(self.player)
            self.update_tiles()  # Обновлять спрайты вдоль камеры
            # Проверять, касаются ли полотенца игрока
            if self.list_victims:
                for i in range(len(self.list_victims)):
                    if self.list_victims[i].collide_with_player() == 1:
                        self.drop.append(self.list_victims[i])
            self.check_victims()
            # Обновлять состояние спрайтов секретного уровня
            secret_group.update()

            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    game_quit()
                    self.running = False
                if event.type == pg.KEYDOWN:
                    # Если все полотенца взяты, то при нажатии SPACE,
                    # игра завершается
                    if event.key == pg.K_SPACE:
                        if self.children <= 0:
                            DrownedChildren().run()
            # Обновление игрока и инвентаря
            all_sprites.update()
            # Затемненные края добавить
            screen.blit(self.overlay, (0, 0))
            self.inventory.render()
            inventory_group.update()
            inventory_group.draw(screen)
            # Индикатор скримера
            self.screamer = random.randint(0, 500)
            # Если полотенца еще остались, то выходит
            # соответствующий текст
            if self.children > 0:
                screen.blit(start_menu_text.render(
                    "Find all " + str(self.children) + " towels",
                    0, (255, 255, 255)), (110, 400))
            # Если все собрано, то игра завершается при нажатии
            # SPACE
            else:
                screen.blit(start_menu_text.render(
                    "PRESS SPACE TO UNCOVER IT",
                    0, (255, 255, 255)), (30, 400))
            # Задержка скримера и его добавление на экран
            if self.screamer >= 495 and (self.player.vx or self.player.vy):
                screen.blit(self.screamer_img, (0, 0))
            # Обновление кадра
            pg.display.flip()
        # Переход в меню
        open_menu()


# Ячейка спрайта игрового поля
class SecretTile(pg.sprite.Sprite):
    def __init__(self, types, x, y, player):
        super().__init__(secret_group)
        self.cell_size = 64  # Размер ячейки
        self.type = types  # Тип ячейки, для загрузки соответсвующего спрайта
        self.image = secret_images[types]  # Загрузка спрайта
        # Изменение размеров ячейки
        self.player = player
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))
        # Прямоугольная маска
        self.rect = self.image.get_rect().move(self.cell_size * x,
                                               self.cell_size * y)

    def collide_with_player(self):
        if self.rect.collidepoint((self.player.rect.x + 32,
                                   self.player.rect.y + 32)):
            if "victim" in self.type:
                pick_up_sound.play()
                return 1


# Функция открытия меню
def open_menu():
    men = Menu()
    men.run()


# Функция выхода из игры, чтобы не было ошибок
def game_quit():
    pg.quit()
    sys.exit()


# Создание частиц
def create_particles(position):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Blood(position, random.choice(numbers), random.choice(numbers))


# Сам запуск всей игры
open_menu()
