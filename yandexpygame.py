import pygame as pg
import os
import sys
import random
import datetime


# Инициализация PyGame(назвал, как pg, чтобы укоротить и не получить PEP8)
pg.init()
pg.mixer.init()

# Название и иконка игры
pg.display.set_caption("Hell Obtained Sensible Tiny And Geniusly Emmy.")
pg.display.set_icon(pg.image.load("sprites\icon.png"))

# Разрешение экрана и залипание клавиш(для передвижения игрока в игре)
screen = pg.display.set_mode((640, 512))
pg.key.set_repeat(500, 10)

# Два варианта текста, которых достаточно для оформления меню
menu_text = pg.font.Font('cyr.ttf', 36)
start_menu_text = pg.font.Font('cyr.ttf', 48)

# Группы спрайтов. Я оформил их отдельно, чтобы изменять поле игры
all_sprites = pg.sprite.Group()
tiles_group = pg.sprite.Group()
entities_group = pg.sprite.Group()
inventory_group = pg.sprite.Group()
drop_group = pg.sprite.Group()
animal_group = pg.sprite.Group()

# Звук клика в меню
click_sound = pg.mixer.Sound("sounds\walk.wav")
click_sound.set_volume(0.4)

# Звук подбора вещей в игре
pick_up_sound = pg.mixer.Sound("sounds\pickup.wav")
pick_up_sound.set_volume(1)

# Звук пожирания мира
world_cut_sound = pg.mixer.Sound("sounds\cut.wav")
world_cut_sound.set_volume(7.0)

# Звук уничтожения природных объектов(трава, камень, цветки и кусты)
entities_destroy = pg.mixer.Sound("sounds\pick.wav")
entities_destroy.set_volume(0.4)

# Звук удара коровки
hit_sound = pg.mixer.Sound("sounds\hit.wav")
hit_sound.set_volume(0.5)

# Звук "быстрого убийства"
cow_died = pg.mixer.Sound("sounds\cow_died.wav")


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


# Словарь спрайтов игрового мира
tile_images = {"grass": load_image('grass.png'),
               "sand": load_image('sand.png'),
               "stone": load_image('stone.png'),
               "empty": load_image('empty_tile.png')}

# Словарь спрайтов секретного уровня
secret_images = {"bath": load_image('bath.png'),
                 "shower": load_image('shower.png'),
                 "right_eye": load_image('eye2.png'),
                 "left_eye": load_image('eye1.png')}

# Словарь спрайтов природных объектов
entity_images = {"green": load_image('green.png'),
                 "flowers": load_image('flowers.png'),
                 "rock": load_image('rock.png'),
                 "bush": load_image('bush.png'),
                 "meat": load_image('meat_entity.png'),
                 "gold_sword": load_image('gold_sword_entity.png'),
                 "silver_sword": load_image('silver_sword_entity.png')}

# Словарь спрайтов инвентаря
inventory_images = {"empty": load_image('empty.png'),
                    "meat_block": load_image('meat_block_inv.png'),
                    "eyes": load_image('eyes_inv.png'),
                    "meat": load_image('meat_inv.png'),
                    "gold": load_image('gold_inv.png'),
                    "gold_sword": load_image('gold_sword_inv.png'),
                    "silver_sword": load_image('silver_sword_inv.png')}

# Словарь спрайтов выпавших вещей
drop_images = {"meat": load_image('meat.png'),
               "gold": load_image('gold.png'),
               "eyes": load_image('eyes.png'),
               "gold_sword": load_image('gold_sword.png'),
               "silver_sword": load_image('silver_sword.png'),
               "meat_block": load_image('meat_block.png')}

# Файлы загрузки результатов
input_score = open("score.txt", "r")
output_score = open("score.txt", "w")

# Переменная отвечает за запуск секретного уровня
psycho_level = 0


# Класс меню
class Menu:
    def __init__(self):
        pg.mouse.set_visible(True)  # Сделать мышь видимой

    def run(self):
        self.running = True
        # Начать игру, Результаты, Настройки и Выход
        start_game = menu_text.render("Start Game", 0, (100, 100, 100))
        start_game_rect = start_game.get_rect().move(80, 150)

        record_txt = menu_text.render("Scores", 0, (100, 100, 100))
        record_rect = record_txt.get_rect().move(80, 200)

        settings_txt = menu_text.render("Settings", 0, (100, 100, 100))
        settings_rect = settings_txt.get_rect().move(80, 250)

        exit_txt = menu_text.render("Quit", 0, (100, 100, 100))
        exit_rect = exit_txt.get_rect().move(80, 300)

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False  # Выход из игры, при закрытии окна

                # Тест секретного уровня
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_u:
                        Drowned_Children().run()

                # Выход из игры нажатием ESC
                if event.type == pg.K_ESCAPE:
                    self.running = False

                # "Анимированные" тексты кнопок меню
                if event.type == pg.MOUSEMOTION:
                    if start_game_rect.collidepoint(event.pos):
                        start_game = menu_text.render("Start Game", 0, (255, 255, 255))
                    else:
                        start_game = menu_text.render("Start Game", 0, (100, 100, 100))

                    if record_rect.collidepoint(event.pos):
                        record_txt = menu_text.render("Scores", 0, (255, 255, 255))
                    else:
                        record_txt = menu_text.render("Scores", 0, (100, 100, 100))

                    if settings_rect.collidepoint(event.pos):
                        settings_txt = menu_text.render("Settings", 0, (255, 255, 255))
                    else:
                        settings_txt = menu_text.render("Settings", 0, (100, 100, 100))

                    if exit_rect.collidepoint(event.pos):
                        exit_txt = menu_text.render("Quit", 0, (255, 255, 255))
                    else:
                        exit_txt = menu_text.render("Quit", 0, (100, 100, 100))

                if event.type == pg.MOUSEBUTTONDOWN:
                    if start_game_rect.collidepoint(event.pos):
                        # Запуск меню выбора уровней
                        click_sound.play()
                        Level().run()

                    if record_rect.collidepoint(event.pos):
                        print(1)
                        click_sound.play()
                    if settings_rect.collidepoint(event.pos):
                        print(2)
                        click_sound.play()
                    if exit_rect.collidepoint(event.pos):
                        # Выход из игры
                        click_sound.play()
                        self.running = False

            # Логотип игры
            image = load_image("logo.png")
            image = pg.transform.scale(image, (144, 196))

            # Обновления кадра, путем заливки
            screen.fill((0, 0, 0))
            # Добавить спрайты на экран
            screen.blit(image, (400, 150))
            screen.blit(start_game, (80, 150))
            screen.blit(record_txt, (80, 200))
            screen.blit(settings_txt, (80, 250))
            screen.blit(exit_txt, (80, 300))
            # Обновление кадра
            pg.display.flip()
        # Выход из игры
        pg.quit()
        sys.exit()


# Выбор уровней
class Level:
    def __init__(self):
        self.level = psycho_level  # Проверка секретного уровня

    def run(self):
        self.running = True
        # Загрузка спрайтов выбора уровней
        self.level_terrain = load_image("level1.png")
        self.level_secret = load_image("level2.png")

        # Маски спрайтов из прямоугольника для клика
        self.level_terrain_rect = self.level_terrain.get_rect().move(0, 120)
        self.level_secret_rect = self.level_secret.get_rect().move(320, 120)

        while self.running:
            for event in pg.event.get():
                # Закрытие экрана
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Запустить обычный игровой мир
                    if self.level_terrain_rect.collidepoint(event.pos):
                        click_sound.play()
                        Tutorial_Terrain().run()
                    # Запустить секретный уровень
                    if self.level_secret_rect.collidepoint(event.pos) and self.level == 1:
                        click_sound.play()
                        self.running = False

            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Добавление объектов на экран
            screen.blit(start_menu_text.render("CHOOSE YOUR LEVEL!",
                                                0, (255, 255, 255)), (110, 20))

            screen.blit(self.level_terrain, (0, 120))
            # Если секретный уровень открыт, добавить его выбор на экран
            if self.level:
                screen.blit(self.level_secret, (320, 120))
            # Обновление кадра
            pg.display.flip()
        # Запуск меню
        open_Menu()


# Туториал для игрового мира
class Tutorial_Terrain:
    def __init__(self):
        self.running = True
        self.slide = 1  # Текущий слайд туториала
        # Если игрок не нажимает на слайд
        # надпись "click" остается
        self.show = False

    def run(self):
        while self.running:
            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Переключение слайдов
                    if self.slide < 7:
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
                        Start_Menu().run()
            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Добавление слайдов
            screen.blit(load_image("t" + str(self.slide) + ".png"), (0, 0))
            if not self.show:
                screen.blit(start_menu_text.render("Click to slide",
                                                   0, (255, 255, 255)), (20, 20))
            # Обновление кадра
            pg.display.flip()
        # Переход в меню
        open_Menu()


# Меню выбора персонажей
class Start_Menu:
    def __init__(self):
        self.gender = ""    # Половая принадлежность
        self.difficult = ""  # Сложность игры

    def run(self):
        self.running = True
        # Персонаж Мартин и его прямоугольная маска
        martin_txt = start_menu_text.render("MARTIN", 0, (100, 100, 100))
        martin_rect = martin_txt.get_rect().move(100, 280)

        # Персонаж Марго и ее прямоугольная маска
        margo_txt = start_menu_text.render("MARGO", 0, (100, 100, 100))
        margo_rect = margo_txt.get_rect().move(400, 280)

        # Легкая сложность
        easy_txt = start_menu_text.render("EASY", 0, (100, 100, 100))
        easy_rect = easy_txt.get_rect().move(60, 400)

        # Средняя сложность
        medium_txt = start_menu_text.render("MEDIUM", 0, (100, 100, 100))
        medium_rect = medium_txt.get_rect().move(240, 400)

        # Высокая сложность
        hardcore_txt = start_menu_text.render("HARD", 0, (100, 100, 100))
        hardcore_rect = hardcore_txt.get_rect().move(470, 400)

        # Картинки персонажей и текст " Выбрать персонажа "
        martin_image = load_image("p.png")
        martin_image = pg.transform.scale(martin_image, (196, 196))

        margo_image = load_image("f.png")
        margo_image = pg.transform.scale(margo_image, (196, 196))

        press_to_start = start_menu_text.render("CHOOSE A CHARACTER!",
                                                0, (255, 255, 255))

        while self.running:
            # Изначально все тексты имеют прозрачность 50 - 60 %
            easy_txt = start_menu_text.render("EASY", 0, (100, 100, 100))
            medium_txt = start_menu_text.render("MEDIUM", 0, (100, 100, 100))
            hardcore_txt = start_menu_text.render("HARD", 0, (100, 100, 100))

            martin_txt = start_menu_text.render("MARTIN", 0, (100, 100, 100))
            margo_txt = start_menu_text.render("MARGO", 0, (100, 100, 100))

            for event in pg.event.get():
                # Закрыть окно
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                    # Запуск игры
                    if event.key == pg.K_SPACE:
                        if self.difficult != "" and self.gender != "":
                            Game(difficult=self.difficult, boyorgirl=self.gender).run()

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Выбор Мартина
                    if martin_rect.collidepoint(event.pos):
                        self.gender = "male"
                        click_sound.play()
                    # Выбор Марго
                    if margo_rect.collidepoint(event.pos):
                        self.gender = "female"
                        click_sound.play()

                    if self.gender:
                        # Если игрок выбрал персонажа, то сложности активны
                        if easy_rect.collidepoint(event.pos):
                            self.difficult = "easy"
                            click_sound.play()
                        if medium_rect.collidepoint(event.pos):
                            self.difficult = "medium"
                            click_sound.play()
                        if hardcore_rect.collidepoint(event.pos):
                            self.difficult = "hardcore"
                            click_sound.play()
            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))

            # Анимация текстов Персонажей
            if self.gender == "female":
                margo_txt = start_menu_text.render("MARGO", 0, (255, 255, 255))

            if self.gender == "male":
                martin_txt = start_menu_text.render("MARTIN", 0, (255, 255, 255))

            # Анимация сложностей
            if self.difficult == "easy":
                easy_txt = start_menu_text.render("EASY", 0, (255, 255, 255))

            if self.difficult == "medium":
                medium_txt = start_menu_text.render("MEDIUM", 0, (255, 255, 255))

            if self.difficult == "hardcore":
                hardcore_txt = start_menu_text.render("HARD", 0, (255, 255, 255))

            # Добавление объектов на экран
            screen.blit(martin_image, (70, 80))
            screen.blit(margo_image, (370, 80))

            screen.blit(martin_txt, (100, 280))
            screen.blit(margo_txt, (400, 280))

            screen.blit(easy_txt, (60, 400))
            screen.blit(medium_txt, (240, 400))
            screen.blit(hardcore_txt, (470, 400))

            # Если игрок выбрал все, что ему нужно
            if self.difficult != "" and self.gender != "":
                press_to_start = start_menu_text.render("PRESS SPACE TO BEGIN!",
                                                        0, (255, 255, 255))
                screen.blit(press_to_start, (70, 20))

            # Если игрок выбрал персонажа
            elif self.difficult == "" and self.gender:
                press_to_start = start_menu_text.render("CHOOSE DIFFUCLTY!",
                                                        0, (255, 255, 255))
                screen.blit(press_to_start, (130, 20))
            # Если игрок только зашел в игру и ничего не выбрал
            elif self.difficult == "" and self.gender == "":
                screen.blit(press_to_start, (110, 20))
            # Обновление кадра
            pg.display.flip()
        # Переход в меню
        open_Menu()


# Окно проигрыша
class Game_Over:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            if psycho_level:
                # Если открыт секретный уровень, будет изменен текст проигрыша
                screen.blit(start_menu_text.render("Children.", 0, (255, 0, 0)),
                            (200, 200))
            else:
                # Если не открыт секретный уровень, будет изменен текст проигрыша
                screen.blit(start_menu_text.render("Game Over", 0, (255, 0, 0)),
                            (200, 200))
            # Обновление кадра
            pg.display.flip()
        # Перейти в меню
        open_Menu()


# Выигрыш игры
class Win:
    def __init__(self, score):
        self.score = score  # Время прохождения игры

    def run(self):
        self.running = True
        # Запись результата в текстовый документ
        output_score.write(str(self.score))
        output_score.close()
        while self.running:

            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Добавление объектов на экран
            screen.blit(start_menu_text.render("You win!", 0, (0, 255, 0)), (200, 200))
            screen.blit(menu_text.render("Your time is", 0, (255, 255, 255)), (225, 250))
            screen.blit(menu_text.render(str(self.score), 0, (255, 255, 255)), (250, 290))
            # Обновление кадра
            pg.display.flip()
        # Запуск меню, при выходе
        open_Menu()


# Выигрыш секретного уровня
class Drowned_Children:
    def __init__(self):
        self.running = True

    def run(self):
        # Загрузка объектов
        child_D = load_image("child_D.png")
        child_D = pg.transform.scale(child_D, (144, 144))

        child_R = load_image("child_R.png")
        child_R = pg.transform.scale(child_R, (144, 144))

        child_O = load_image("child_O.png")
        child_O = pg.transform.scale(child_O, (144, 144))

        child_W = load_image("child_W.png")
        child_W = pg.transform.scale(child_W, (144, 144))

        child_N = load_image("child_N.png")
        child_N = pg.transform.scale(child_N, (144, 144))
        while self.running:
            for event in pg.event.get():
                # Закрытие окна
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    # Перейти в меню
                    if event.key == pg.K_ESCAPE:
                        self.running = False

            # Обновление кадра, путем заливки
            screen.fill((0, 0, 0))
            # Добавление объектов на экран
            screen.blit(child_D, (60, 70))
            screen.blit(child_R, (156, 70))
            screen.blit(child_O, (252, 70))
            screen.blit(child_W, (348, 70))
            screen.blit(child_N, (444, 70))

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
        open_Menu()


# Игровой мир (Уровень 1)
class Game:
    def __init__(self, difficult="easy", boyorgirl="male"):
        # Очистить все поле, при старте новой игры
        self.clear_tiles()
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

        posx = 0
        posy = 0

        self.gold = 0
        self.silver_sword = 0
        self.is_gold_sword = random.randint(0, 100)
        self.is_silver_sword = random.randint(0, 100)
        self.gold_sword = 0

        quarter = random.randint(1, 4)

        if quarter == 1:
            posx = random.randint(1, 15)
            posy = random.randint(1, 15)

        if quarter == 2:
            posx = random.randint(16, 31)
            posy = random.randint(16, 31)

        if quarter == 3:
            posx = random.randint(32, 47)
            posy = random.randint(32, 47)

        if quarter == 4:
            posx = random.randint(48, 62)
            posy = random.randint(48, 62)

        self.player = Player(all_sprites, self, posx - 0.5, posy - 0.5, 64, boyorgirl)
        self.camera = Camera()
        self.inventory = Inventory()
        self.craft = Craft()

        self.mobs = []
        for _ in range(random.randint(18, 24)):
            self.mobs.append(Cow(animal_group,
                                 self, random.randint(2, 62), random.randint(2, 62), 64))
        self.drop = []

        if self.difficult == "easy":
            self.cell_timer = 15
        if self.difficult == "medium":
            self.cell_timer = 7.5
        if self.difficult == "hardcore":
            self.cell_timer = 3.75

        self.current_cursor_pos = 0

    def clear_tiles(self):
        entities_group.empty()
        tiles_group.empty()
        all_sprites.empty()
        animal_group.empty()
        drop_group.empty()
        inventory_group.empty()

    def player_run(self):
        self.player.state = "run"
        self.player.timer = 0.05
        self.gender()

    def gender(self):
        if self.player.gender == "male":
            if self.player.mirrored:
                self.player.cut_sheet(load_image("pm_sheet.png"))
            else:
                self.player.cut_sheet(load_image("p_sheet.png"))
        else:
            if self.player.mirrored:
                self.player.cut_sheet(load_image("fm_sheet.png"))
            else:
                self.player.cut_sheet(load_image("f_sheet.png"))

    def player_stay(self):
        self.player.state = "stay"
        self.player.timer = 0.5
        self.gender()

    def update_tiles(self):
        for sprite in tiles_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in entities_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in animal_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in drop_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

    def world_cutting(self):
        self.timer_cut += self.dt
        if self.timer_cut > self.cell_timer:
            self.step += 1

            for i in range(self.world.w):
                self.world.world_array[self.step - 1][i] = -1
                self.world.world_array[-self.step][i] = -1

            for i in range(self.world.h):
                self.world.world_array[i][self.step - 1] = -1
                self.world.world_array[i][-self.step] = -1

            self.world.render()

            tiles_group.update()
            entities_group.update()
            animal_group.update()

            world_cut_sound.play()
            self.timer_cut = 0

    def check_cows(self):
        for i in range(len(self.mobs)):
            # Если животное касается границ, то оно отлетает
            if self.mobs[i].rect.x < 64 * self.step:
                self.mobs[i].vx += 8
            if self.mobs[i].rect.x > 64 * (65 - self.step):
                self.mobs[i].vx -= 8
            if self.mobs[i].rect.y < 64 * self.step:
                self.mobs[i].vy += 8
            if self.mobs[i].rect.y > 64 * (65 - self.step):
                self.mobs[i].vy -= 8

        for i in range(len(self.mobs)):
            for j in range(len(self.mobs)):
                if self.mobs[i] != self.mobs[j]:
                    # Если животное касается других, то оно отлетает
                    if self.mobs[i].rect.collidepoint(self.mobs[j].rect.topleft):
                        if self.mobs[i].rect.x + 32 < self.mobs[j].rect.x:
                            self.mobs[i].vy += 5
                            self.mobs[j].vy -= 5

                        if self.mobs[i].rect.x + 32 > self.mobs[j].rect.x:
                            self.mobs[i].vy -= 5
                            self.mobs[j].vy += 5

                        if self.mobs[i].rect.y + 32 < self.mobs[j].rect.y:
                            self.mobs[i].vy += 5
                            self.mobs[j].vy -= 5

                        if self.mobs[i].rect.y + 32 > self.mobs[j].rect.y:
                            self.mobs[i].vy -= 5
                            self.mobs[j].vy += 5

    def append_drop(self, x, y):
        b = random.randint(0, 100)
        if self.is_gold_sword < 50:
            if b < 30 and self.gold < 2:
                self.drop.append(Drop("gold", self.player, x, y, self))
                self.gold += 1

        if self.is_gold_sword >= 50:
            if b >= 70 and self.gold_sword < 1:
                self.drop.append(Drop("gold_sword", self.player, x, y, self))
                self.gold_sword += 1

        if self.is_silver_sword >= 50:
            if b == 100 and self.silver_sword < 1:
                self.drop.append(Drop("silver_sword", self.player, x, y, self))
                self.silver_sword += 1

    def append_drop_block(self, x, y, i):
        if i == 5:
            self.drop.append(Drop("meat_block", self.player, x, y, self))
        if i == 6:
            self.drop.append(Drop("gold_sword", self.player, x, y, self))
        if i == 7:
            self.drop.append(Drop("silver_sword", self.player, x, y, self))

    def cow_and_player(self):
        self.tmpmobs = []
        for i in range(len(self.mobs)):
            if self.mobs[i].rect.colliderect(self.player.rect):
                if self.tool == "axe":
                    self.mobs[i].hp -= 2
                    hit_sound.play()
                else:
                    self.mobs[i].hp -= 1
                    hit_sound.play()

                if self.mobs[i].check_hp():
                    cow_died.play()
                    self.mobs[i].kill()
                    drop_group.update()
                    if self.tool == "axe":
                        self.drop.append(Drop("meat", self.player, int((self.player.rect.x + 32) / 4096 * 64)
                                              , int((self.player.rect.y + 32) / 4096 * 64), self))
                    else:
                        self.drop.append(Drop("eyes", self.player, int((self.player.rect.x + 32) / 4096 * 64)
                                              , int((self.player.rect.y + 32) / 4096 * 64), self))
                    self.tmpmobs.append(i)

        if self.tmpmobs:
            for i in range(len(self.tmpmobs)):
                del self.mobs[self.tmpmobs[i]]

        self.tmpmobs.clear()

    def craft_checking(self):
        for i in range(self.inventory.w):
            if self.inventory.inv[0][i] == "meat" or self.inventory.inv[0][i] == "eyes":
                if self.current_cursor_pos == i:
                    if self.inventory.check_craft_meat():
                        self.craft.craft_type = 0
            if self.inventory.inv[0][i] == "gold":
                if self.current_cursor_pos == i:
                    if self.inventory.check_craft_gold():
                        self.craft.craft_type = 1

    def drop_clean(self):
        if self.drop:
            for i in range(len(self.drop)):
                if self.drop[i].check_drop_pos() == 1:
                    self.drop[i].kill()
                    self.tmplist.remove(i)

                if self.drop[i].get_event() == 1:
                    self.drop[i].kill()
                    self.inventory.append(self.drop[i].type)
                    self.tmplist.append(i)

        if self.tmplist:
            for i in range(len(self.tmplist)):
                del self.drop[self.tmplist[i]]

        self.tmplist.clear()

    def put_block(self, block):
        b = 0
        index1 = 0
        for i in range(self.inventory.w):
            if self.inventory.inv[0][i] == block and \
                    self.inventory.inv[1][i] > 0:
                b += 1
                index1 = i
        if b:
            self.inventory.inv[1][index1] -= 1
            if self.inventory.inv[1][index1] == 0:
                self.inventory.invtmp.remove(self.inventory.inv[0][index1])
                self.inventory.inv[0][index1] = 0

    def run(self):
        # Загружаю мир и инвентарь
        self.world.render()
        self.inventory.render()
        self.running = True

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

        # Лист, чтобы прослеживать уже добавленные предметы
        self.tmplist = []

        # Загрузка курсора инвентаря
        self.cursor = load_image("cursor.png")
        self.cursor = pg.transform.scale(self.cursor, (72, 72))
        while self.running:
            screen.fill((0, 0, 0))
            if not self.pause:
                pg.mouse.set_visible(False)
                self.dt = self.clock.tick(self.FPS) / 1000

                self.time_in_game += self.dt
                self.world_cutting()
                self.camera.update(self.player)
                self.update_tiles()

                # Кравт отображение
                self.craft.craft_type = -1
                self.craft_checking()
                self.craft.render()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.MOUSEMOTION:
                    if self.pause:
                        if continue_rect.collidepoint(event.pos):
                            continue_txt = start_menu_text.render("Continue", 0, (255, 255, 255))
                        else:
                            continue_txt = start_menu_text.render("Continue", 0, (100, 100, 100))

                        if quit_rect.collidepoint(event.pos):
                            quit_txt = start_menu_text.render("Quit", 0, (255, 255, 255))
                        else:
                            quit_txt = start_menu_text.render("Quit", 0, (100, 100, 100))

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.pause:
                            if continue_rect.collidepoint(event.pos):
                                self.pause = False

                            if quit_rect.collidepoint(event.pos):
                                self.running = False

                if event.type == pg.KEYDOWN:
                    # Очистка дропа, если касается игрок.
                    self.drop_clean()
                    # Сверху, очистки блок

                    if not self.pause:
                        if event.key == pg.K_ESCAPE:
                            self.pause = True

                        #  Уничтожение блоков
                        if event.key == pg.K_SPACE:
                            ifdestroy = False
                            x = int((self.player.rect.x + 32) / 4096 * 64)
                            y = int((self.player.rect.y + 32) / 4096 * 64)

                            # Влево
                            if 0 < self.world.entities[y][x - 1] < 5:
                                self.world.entities[y][x - 1] = 0
                                self.append_drop(x - 1, y)
                                ifdestroy = True

                            if self.world.entities[y][x - 1] == 5:
                                self.world.entities[y][x - 1] = 0
                                self.append_drop_block(x - 1, y, 5)
                                ifdestroy = True

                            if self.world.entities[y][x - 1] == 6:
                                self.world.entities[y][x - 1] = 0
                                self.append_drop_block(x - 1, y, 6)
                                ifdestroy = True

                            if self.world.entities[y][x - 1] == 7:
                                self.world.entities[y][x - 1] = 0
                                self.append_drop_block(x - 1, y, 7)
                                ifdestroy = True

                            # Вправо
                            if 0 < self.world.entities[y][x + 1] < 5:
                                self.world.entities[y][x + 1] = 0
                                self.append_drop(x + 1, y)
                                ifdestroy = True

                            if self.world.entities[y][x + 1] == 5:
                                self.world.entities[y][x + 1] = 0
                                self.append_drop_block(x + 1, y, 5)
                                ifdestroy = True

                            if self.world.entities[y][x + 1] == 6:
                                self.world.entities[y][x + 1] = 0
                                self.append_drop_block(x + 1, y, 6)
                                ifdestroy = True

                            if self.world.entities[y][x + 1] == 7:
                                self.world.entities[y][x + 1] = 0
                                self.append_drop_block(x + 1, y, 7)
                                ifdestroy = True

                            # Снизу
                            if 0 < self.world.entities[y + 1][x] < 5:
                                self.world.entities[y + 1][x] = 0
                                self.append_drop(x, y + 1)
                                ifdestroy = True

                            if self.world.entities[y + 1][x] == 5:
                                self.world.entities[y + 1][x] = 0
                                self.append_drop_block(x, y + 1, 5)
                                ifdestroy = True

                            if self.world.entities[y + 1][x] == 6:
                                self.world.entities[y + 1][x] = 0
                                self.append_drop_block(x, y + 1, 6)
                                ifdestroy = True

                            if self.world.entities[y + 1][x] == 7:
                                self.world.entities[y + 1][x] = 0
                                self.append_drop_block(x, y + 1, 7)
                                ifdestroy = True

                            # Сверху
                            if 0 < self.world.entities[y - 1][x] < 5:
                                self.world.entities[y - 1][x] = 0
                                self.append_drop(x, y - 1)
                                ifdestroy = True

                            if self.world.entities[y - 1][x] == 5:
                                self.world.entities[y - 1][x] = 0
                                self.append_drop_block(x, y - 1, 5)
                                ifdestroy = True

                            if self.world.entities[y - 1][x] == 6:
                                self.world.entities[y - 1][x] = 0
                                self.append_drop_block(x, y - 1, 6)
                                ifdestroy = True

                            if self.world.entities[y - 1][x] == 7:
                                self.world.entities[y - 1][x] = 0
                                self.append_drop_block(x, y - 1, 7)
                                ifdestroy = True

                            # По центру
                            if 0 < self.world.entities[y][x] < 5:
                                self.world.entities[y][x] = 0
                                self.append_drop(x, y)
                                ifdestroy = True

                            if self.world.entities[y][x] == 5:
                                self.world.entities[y][x] = 0
                                self.append_drop_block(x, y, 5)
                                ifdestroy = True

                            if self.world.entities[y][x] == 6:
                                self.world.entities[y][x] = 0
                                self.append_drop_block(x, y, 6)
                                ifdestroy = True

                            if self.world.entities[y][x] == 7:
                                self.world.entities[y][x] = 0
                                self.append_drop_block(x, y, 7)
                                ifdestroy = True

                            # Само уничтожение
                            if ifdestroy:
                                self.world.render()
                                entities_destroy.play()
                                entities_group.update()
                                drop_group.update()
                                ifdestroy = False

                        if event.key == pg.K_m:
                            x = int((self.player.rect.x + 32) / 4096 * 64)
                            y = int((self.player.rect.y + 32) / 4096 * 64)

                            for i in range(self.inventory.w):
                                if self.inventory.inv[0][i] == "meat_block":
                                    if self.current_cursor_pos == i:
                                        if self.player.mirrored:
                                            if self.world.entities[y][x + 1] < 5:
                                                self.world.entities[y][x + 1] = 5
                                                self.world.render()
                                                entities_group.update()
                                                self.put_block("meat_block")
                                        else:
                                            if self.world.entities[y][x - 1] < 5:
                                                self.world.entities[y][x - 1] = 5
                                                self.world.render()
                                                entities_group.update()
                                                self.put_block("meat_block")

                                if self.inventory.inv[0][i] == "gold_sword":
                                    if self.current_cursor_pos == i:
                                        if self.player.mirrored:
                                            if self.world.entities[y][x + 1] < 5:
                                                self.world.entities[y][x + 1] = 6
                                                self.world.render()
                                                entities_group.update()
                                                self.put_block("gold_sword")
                                        else:
                                            if self.world.entities[y][x - 1] < 5:
                                                self.world.entities[y][x - 1] = 6
                                                self.world.render()
                                                entities_group.update()
                                                self.put_block("gold_sword")

                                if self.inventory.inv[0][i] == "silver_sword":
                                    if self.current_cursor_pos == i:
                                        if self.player.mirrored:
                                            if self.world.entities[y][x + 1] < 5:
                                                self.world.entities[y][x + 1] = 7
                                                self.world.render()
                                                entities_group.update()
                                                self.put_block("silver_sword")
                                        else:
                                            if self.world.entities[y][x - 1] < 5:
                                                self.world.entities[y][x - 1] = 7
                                                self.world.render()
                                                entities_group.update()
                                                self.put_block("silver_sword")
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
                            b = 0
                            index1 = 0
                            index2 = 0
                            if self.craft.craft_type == 0:
                                for i in range(self.inventory.w):
                                    if self.inventory.inv[0][i] == "meat" and self.inventory.inv[1][i] > 0:
                                        b += 1
                                        index1 = i
                                    if self.inventory.inv[0][i] == "eyes" and self.inventory.inv[1][i] > 0:
                                        b += 1
                                        index2 = i
                                if b == 2:
                                    self.inventory.inv[1][index1] -= 1
                                    self.inventory.inv[1][index2] -= 1
                                    if self.inventory.inv[1][index1] == 0:
                                        self.inventory.invtmp.remove(self.inventory.inv[0][index1])
                                        self.inventory.inv[0][index1] = 0

                                    if self.inventory.inv[1][index2] == 0:
                                        self.inventory.invtmp.remove(self.inventory.inv[0][index2])
                                        self.inventory.inv[0][index2] = 0

                                    self.inventory.append("meat_block")

                            if self.craft.craft_type == 1:
                                for i in range(self.inventory.w):
                                    if self.inventory.inv[0][i] == "gold" and self.inventory.inv[1][i] > 1:
                                        b += 1
                                        index1 = i
                                if b:
                                    self.inventory.inv[1][index1] -= 2
                                    if self.inventory.inv[1][index1] == 0:
                                        self.inventory.invtmp.remove(self.inventory.inv[0][index1])
                                        self.inventory.inv[0][index1] = 0

                                    self.inventory.append("gold_sword")

                        # Изменение положения курсора в инвентаре
                        if event.key == pg.K_p:
                            # Если курсор еще не в конце инветаря
                            if self.current_cursor_pos < self.inventory.w - 1:
                                self.current_cursor_pos += 1
                            # Если курсор уже на последней ячейке, то он переходит на первую
                            else:
                                self.current_cursor_pos = 0  # Сброс курсора

            if self.pause:
                # Когда пауза, курсор и кнопки: Продолжить, Выйти - активированы
                pg.mouse.set_visible(True)
                # Добавление кнопок меню паузы на экран
                screen.blit(continue_txt, (60, 100))  # Продолжить
                screen.blit(quit_txt, (60, 160))  # Выйти

            if not self.pause:
                # Если весь мир сожран, то игра завершается с проигрышем
                if self.step == 33:
                    Game_Over().run()

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
                                    self.world.entities[j + 2][i] == 5 and \
                                    self.world.entities[j + 2][i + 1] == 5 and \
                                    self.world.entities[j + 2][i + 2] == 5:
                                Win(str(datetime.timedelta(seconds=int(self.time_in_game)))).run()
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
                                    self.world.entities[j + 2][i + 1] == 5 and \
                                    self.world.entities[j + 2][i + 2] == 5:
                                global psycho_level
                                psycho_level = 1
                                Game_Over().run()

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
                screen.blit(start_menu_text.render(str(self.tool),
                                                   0, (255, 255, 255)), (64, 72))
                screen.blit(axe_scissors, (64, 0))
                screen.blit(self.cursor, (72 * self.current_cursor_pos + 240, 0))
            # Обновление кадра
            pg.display.flip()
        # Запуск меню
        open_Menu()


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
                Inventory_Tile('empty', i)
            # Слот с золотом
            if self.inv[0][i] == "gold" and self.inv[1][i] != 0:
                Inventory_Tile('gold', i)
            # Слот с серебрянным мечом
            if self.inv[0][i] == "silver_sword" and self.inv[1][i] != 0:
                Inventory_Tile('silver_sword', i)
            # Слот с золотым мечом
            if self.inv[0][i] == "gold_sword" and self.inv[1][i] != 0:
                Inventory_Tile('gold_sword', i)
            # Слот с мясом
            if self.inv[0][i] == "meat" and self.inv[1][i] != 0:
                Inventory_Tile('meat', i)
            # Слот с глазами
            if self.inv[0][i] == "eyes" and self.inv[1][i] != 0:
                Inventory_Tile('eyes', i)
            # Слот с сухожилием
            if self.inv[0][i] == "meat_block" and self.inv[1][i] != 0:
                Inventory_Tile('meat_block', i)
            # Добавление ячеек инвентаря на экран
            screen.blit(start_menu_text.render(str(self.inv[1][i]),
                                               0, (255, 255, 255)),
                        (284 + (i * 72), 72))

    def append(self, type):
        # Добавление вещей в инвентарь
        for i in range(self.w):
            # Если такого предмета нет в инвентаре, он попадает в новый слот
            if type not in self.invtmp:
                if self.inv[0][i] == 0:
                    self.inv[0][i] = type
                    self.inv[1][i] += 1
                    self.invtmp.append(type)
            # Если такой предмет существует в инвентаре, он прибавляется
            else:
                if self.inv[0][i] == type:
                    self.inv[0][i] = type
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
class Inventory_Tile(pg.sprite.Sprite):
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


# Коровка
class Cow(pg.sprite.Sprite):
    def __init__(self, group, game, x, y, cell_size):
        super().__init__(group)
        self.game = game    # привязанный параметр текущей игры
        self.state = "stay"  # текущее положение, для анимации
        self.tmpstate = False  # буферное положение, для переключения анимации

        self.frames = []    # Лист кадров
        self.cur_frame = 0  # Текущий кадр

        self.cut_sheet(load_image("c_sheet.png"))   # Полотно спрайтов коровки

        self.image = self.frames[self.cur_frame]    # Картинка из листа
        self.size = self.image.get_size()   # Получить размер картинки

        self.rect = self.image.get_rect()   # Получить маску из прямоугольника
        self.cell_size = cell_size  # Текущий размер клетки в игровом мире

        self.speed = 100    # Скорость коровки

        self.vx = 0  # Скорость коровки на проекцию Ox
        self.vy = 0  # Скорость коровки на проекцию Oy

        self.timer = 0  # Таймер переключения анимаций
        self.timer_choose_animation = 0  # Таймер свободного движения коровки

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
            self.cut_sheet(load_image("c_sheet.png"))

        # Если коровка идет налево
        if b == 1:
            self.vx = -self.speed

        # Если коровка идет направо
        if b == 2:
            self.vx = self.speed

        # Если коровка идет вверх
        if b == 3:
            self.vy = -self.speed

        # Если коровка идет вниз
        if b == 4:
            self.vy = self.speed

        # Если коровка не стоит, то проигрывается анимация бега
        if b > 0:
            self.state = "run"
            self.cut_sheet(load_image("c_sheet.png"))

    def update(self):
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


class Secret_Level:
    def __init__(self):
        self.dt = 0
        self.FPS = 100
        self.clock = pg.time.Clock()
        self.children = 0
        self.drop = []
        self.inventory = Inventory()
        self.camera = Camera()

    def update_tiles(self):
        for sprite in tiles_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in drop_group:
            screen.blit(sprite.image, self.camera.apply(sprite))

    def drop_clean(self):
        if self.drop:
            for i in range(len(self.drop)):
                if self.drop[i].get_event() == 1:
                    self.drop[i].kill()
                    self.inventory.append(self.drop[i].type)
                    self.tmplist.append(i)

        if self.tmplist:
            for i in range(len(self.tmplist)):
                del self.drop[self.tmplist[i]]

        self.tmplist.clear()

    def run(self):
        # Загружаю мир и инвентарь
        self.world.render()
        self.inventory.render()
        self.running = True

        # Обновляю группы спрайтов
        all_sprites.update()
        inventory_group.update()
        drop_group.update()

        # Кнопки паузы
        continue_txt = start_menu_text.render("Continue", 0, (100, 100, 100))
        continue_rect = continue_txt.get_rect().move(60, 100)

        quit_txt = start_menu_text.render("Quit", 0, (100, 100, 100))
        quit_rect = quit_txt.get_rect().move(60, 160)

        # Лист, чтобы прослеживать уже добавленные предметы
        self.tmplist = []

        self.cursor = load_image("cursor.png")
        self.cursor = pg.transform.scale(self.cursor, (72, 72))
        while self.running:
            screen.fill((0, 0, 0))
            if not self.pause:
                pg.mouse.set_visible(False)
                self.dt = self.clock.tick(self.FPS) / 1000

                self.camera.update(self.player)
                self.update_tiles()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.MOUSEMOTION:
                    if self.pause:
                        if continue_rect.collidepoint(event.pos):
                            continue_txt = start_menu_text.render("Continue", 0, (255, 255, 255))
                        else:
                            continue_txt = start_menu_text.render("Continue", 0, (100, 100, 100))

                        if quit_rect.collidepoint(event.pos):
                            quit_txt = start_menu_text.render("Quit", 0, (255, 255, 255))
                        else:
                            quit_txt = start_menu_text.render("Quit", 0, (100, 100, 100))

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.pause:
                            if continue_rect.collidepoint(event.pos):
                                self.pause = False

                            if quit_rect.collidepoint(event.pos):
                                self.running = False

                if event.type == pg.KEYDOWN:
                    self.drop_clean()
                    if not self.pause:
                        if event.key == pg.K_p:
                            if self.current_cursor_pos < self.inventory.w - 1:
                                self.current_cursor_pos += 1
                            else:
                                self.current_cursor_pos = 0

                if event.type == pg.KEYUP:
                    if not self.pause:
                        if event.key == pg.K_a or event.key == pg.K_w \
                                or event.key == pg.K_s or event.key == pg.K_d:
                            self.player_stay()

            if self.pause:
                pg.mouse.set_visible(True)

                screen.blit(continue_txt, (60, 100))
                screen.blit(quit_txt, (60, 160))

            if not self.pause:
                if self.children == 5:
                    Drowned_Children().run()
                all_sprites.update()
                self.inventory.render()
                inventory_group.update()
                inventory_group.draw(screen)
                screen.blit(self.cursor, (72 * self.current_cursor_pos + 240, 0))

            pg.display.flip()
        open_Menu()


# Функция открытия меню
def open_Menu():
    men = Menu()
    men.run()


# Функция выхода из игры, чтобы не было ошибок
def quit():
    pg.quit()
    sys.exit()


# Сам запуск всей игры
open_Menu()