import pygame as pg
import os
import sys
import random
import datetime


pg.init()
pg.mixer.init()

pg.display.set_caption("Hell Obtained Sensible Tiny And Geniusly Emmy.")
pg.display.set_icon(pg.image.load("sprites\icon.png"))
WIDTH = 640
HEIGHT = 512
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.key.set_repeat(500, 100)

menu_text = pg.font.Font('cyr.ttf', 36)
start_menu_text = pg.font.Font('cyr.ttf', 48)

all_sprites = pg.sprite.Group()
tiles_group = pg.sprite.Group()
entities_group = pg.sprite.Group()
inventory_group = pg.sprite.Group()
drop_group = pg.sprite.Group()
animal_group = pg.sprite.Group()

walk_sound = pg.mixer.Sound("sounds\walk2.wav")
walk_sound.set_volume(0.1)

click_sound = pg.mixer.Sound("sounds\walk.wav")
click_sound.set_volume(0.4)

world_cut_sound = pg.mixer.Sound("sounds\cut.wav")
world_cut_sound.set_volume(7.0)

entities_destroy = pg.mixer.Sound("sounds\cow_walk.wav")
entities_destroy.set_volume(0.3)


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


tile_images = {"grass": load_image('grass.png'),
               "sand": load_image('sand.png'),
               "stone": load_image('stone.png'),
               "empty": load_image('empty_tile.png')}

entity_images = {"green": load_image('green.png'),
                 "flowers": load_image('flowers.png'),
                 "rock": load_image('rock.png'),
                 "bush": load_image('bush.png')}

inventory_images = {"empty": load_image('empty.png'),
                    "meat_block": load_image('meat_block_inv.png'),
                    "eyes": load_image('eyes_inv.png'),
                    "meat": load_image('meat_inv.png'),
                    "gold": load_image('gold_inv.png'),
                    "gold_sword": load_image('gold_sword_inv.png'),
                    "silver_sword": load_image('silver_sword_inv.png')}

drop_images = {"meat": load_image('meat.png')}


class Menu:
    def __init__(self):
        pg.mouse.set_visible(True)

    def run(self):
        self.running = True
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
                    self.running = False

                if event.type == pg.K_ESCAPE:
                    self.running = False
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
                        click_sound.play()
                        begin_game = Start_Menu()
                        begin_game.run()

                    if record_rect.collidepoint(event.pos):
                        print(1)
                        click_sound.play()
                    if settings_rect.collidepoint(event.pos):
                        print(2)
                        click_sound.play()
                    if exit_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.running = False

            image = load_image("logo.png")
            image = pg.transform.scale(image, (144, 196))

            screen.fill((0, 0, 0))
            screen.blit(image, (400, 150))
            screen.blit(start_game, (80, 150))
            screen.blit(record_txt, (80, 200))
            screen.blit(settings_txt, (80, 250))
            screen.blit(exit_txt, (80, 300))

            pg.display.flip()
        pg.quit()
        sys.exit()


class Start_Menu:
    def __init__(self):
        self.gender = ""
        self.difficult = ""

    def run(self):
        self.running = True
        martin_txt = start_menu_text.render("MARTIN", 0, (100, 100, 100))
        martin_rect = martin_txt.get_rect().move(100, 280)

        margo_txt = start_menu_text.render("MARGO", 0, (100, 100, 100))
        margo_rect = margo_txt.get_rect().move(400, 280)

        easy_txt = start_menu_text.render("EASY", 0, (100, 100, 100))
        easy_rect = easy_txt.get_rect().move(60, 400)

        medium_txt = start_menu_text.render("MEDIUM", 0, (100, 100, 100))
        medium_rect = medium_txt.get_rect().move(240, 400)

        hardcore_txt = start_menu_text.render("HARD", 0, (100, 100, 100))
        hardcore_rect = hardcore_txt.get_rect().move(470, 400)

        martin_image = load_image("p.png")
        martin_image = pg.transform.scale(martin_image, (196, 196))

        margo_image = load_image("f.png")
        margo_image = pg.transform.scale(margo_image, (196, 196))

        press_to_start = start_menu_text.render("CHOOSE A CHARACTER!",
                                                0, (255, 255, 255))

        while self.running:
            easy_txt = start_menu_text.render("EASY", 0, (100, 100, 100))
            medium_txt = start_menu_text.render("MEDIUM", 0, (100, 100, 100))
            hardcore_txt = start_menu_text.render("HARD", 0, (100, 100, 100))

            martin_txt = start_menu_text.render("MARTIN", 0, (100, 100, 100))
            margo_txt = start_menu_text.render("MARGO", 0, (100, 100, 100))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                    if event.key == pg.K_SPACE:
                        if self.difficult != "" and self.gender != "":
                            Game(difficult=self.difficult, boyorgirl=self.gender).run()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if martin_rect.collidepoint(event.pos):
                        self.gender = "male"
                        click_sound.play()
                    if margo_rect.collidepoint(event.pos):
                        self.gender = "female"
                        click_sound.play()

                    if self.gender:
                        if easy_rect.collidepoint(event.pos):
                            self.difficult = "easy"
                            click_sound.play()
                        if medium_rect.collidepoint(event.pos):
                            self.difficult = "medium"
                            click_sound.play()
                        if hardcore_rect.collidepoint(event.pos):
                            self.difficult = "hardcore"
                            click_sound.play()

            screen.fill((0, 0, 0))

            if self.gender == "female":
                margo_txt = start_menu_text.render("MARGO", 0, (255, 255, 255))

            if self.gender == "male":
                martin_txt = start_menu_text.render("MARTIN", 0, (255, 255, 255))

            if self.difficult == "easy":
                easy_txt = start_menu_text.render("EASY", 0, (255, 255, 255))

            if self.difficult == "medium":
                medium_txt = start_menu_text.render("MEDIUM", 0, (255, 255, 255))

            if self.difficult == "hardcore":
                hardcore_txt = start_menu_text.render("HARD", 0, (255, 255, 255))

            screen.blit(martin_image, (70, 80))
            screen.blit(margo_image, (370, 80))

            screen.blit(martin_txt, (100, 280))
            screen.blit(margo_txt, (400, 280))

            screen.blit(easy_txt, (60, 400))
            screen.blit(medium_txt, (240, 400))
            screen.blit(hardcore_txt, (470, 400))

            if self.difficult != "" and self.gender != "":
                press_to_start = start_menu_text.render("PRESS SPACE TO BEGIN!",
                                                        0, (255, 255, 255))
                screen.blit(press_to_start, (70, 20))

            elif self.difficult == "" and self.gender:
                press_to_start = start_menu_text.render("CHOOSE DIFFUCLTY!",
                                                        0, (255, 255, 255))
                screen.blit(press_to_start, (130, 20))
            elif self.difficult == "" and self.gender == "":
                screen.blit(press_to_start, (110, 20))

            pg.display.flip()
        open_Menu()


class Game:  # Инициализация игры
    def __init__(self, difficult="easy", boyorgirl="male"):
        self.clear_tiles()

        self.pause = False
        self.dt = 0
        self.FPS = 100
        self.clock = pg.time.Clock()
        self.timer_cut = 0
        self.time_in_game = 0
        self.mousepos = (0, 0)
        self.difficult = difficult
        self.step = 1

        self.world = TileMap()
        self.inventory = Inventory()

        posx = 0
        posy = 0

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

        self.mobs = []
        for _ in range(random.randint(24, 32)):
            self.mobs.append(Cow(animal_group,
                                 self, random.randint(2, 62), random.randint(2, 62), 64))

        if self.difficult == "easy":
            self.cell_timer = 15
        if self.difficult == "medium":
            self.cell_timer = 7.5
        if self.difficult == "hardcore":
            self.cell_timer = 3.75

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
        for sprite in drop_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in tiles_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in entities_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in animal_group:
            screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))

    def world_cutting(self):
        self.timer_cut += self.dt
        if self.timer_cut > self.cell_timer:
            self.step += 1

            for i in range(self.world.w):
                self.world.board[self.step - 1][i] = -1
                self.world.board[-self.step][i] = -1

            for i in range(self.world.h):
                self.world.board[i][self.step - 1] = -1
                self.world.board[i][-self.step] = -1

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
                self.mobs[i].vx += 10
            if self.mobs[i].rect.x > 64 * (65 - self.step):
                self.mobs[i].vx -= 10
            if self.mobs[i].rect.y < 64 * self.step:
                self.mobs[i].vy += 10
            if self.mobs[i].rect.y > 64 * (65 - self.step):
                self.mobs[i].vy -= 10

        for i in range(len(self.mobs)):
            for j in range(len(self.mobs)):
                if self.mobs[i] != self.mobs[j]:
                    # Если животное касается других, то оно отлетает
                    if self.mobs[i].rect.collidepoint(self.mobs[j].rect.topleft):
                        if self.mobs[i].rect.x + 64 < self.mobs[j].rect.x:
                            self.mobs[i].vy += 5
                            self.mobs[j].vy -= 5

                        if self.mobs[i].rect.x + 64 > self.mobs[j].rect.x:
                            self.mobs[i].vy -= 5
                            self.mobs[j].vy += 5

                        if self.mobs[i].rect.y + 64 < self.mobs[j].rect.y:
                            self.mobs[i].vy += 5
                            self.mobs[j].vy -= 5

                        if self.mobs[i].rect.y + 64 > self.mobs[j].rect.y:
                            self.mobs[i].vy -= 5
                            self.mobs[j].vy += 5

    def run(self):
        self.world.render()
        self.inventory.render()
        self.running = True

        tiles_group.update()
        all_sprites.update()
        animal_group.update()
        inventory_group.update()
        entities_group.update()

        # Кнопки паузы
        continue_txt = start_menu_text.render("Continue", 0, (100, 100, 100))
        continue_rect = continue_txt.get_rect().move(60, 100)

        quit_txt = start_menu_text.render("Quit", 0, (100, 100, 100))
        quit_rect = quit_txt.get_rect().move(60, 160)

        while self.running:
            screen.fill((0, 0, 0))
            if not self.pause:
                pg.mouse.set_visible(False)
                self.dt = self.clock.tick(self.FPS) / 1000

                self.time_in_game += self.dt
                self.world_cutting()
                self.camera.update(self.player)
                self.update_tiles()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                    self.running = False

                if event.type == pg.MOUSEMOTION:
                    if pg.mouse.get_focused():
                        self.mousepos = event.pos
                        if self.mousepos[0] < 320:
                            self.player.mirrored = False
                        else:
                            self.player.mirrored = True

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
                    if not self.pause:
                        if event.key == pg.K_ESCAPE:
                            self.pause = True

                        if event.key == pg.K_a or event.key == pg.K_w \
                                or event.key == pg.K_s or event.key == pg.K_d:
                            self.player_run()

                        if event.key == pg.K_SPACE:
                            ifdestroy = False
                            x = int((self.player.rect.x + 32) / 4096 * 64)
                            y = int((self.player.rect.y + 32) / 4096 * 64)

                            if self.world.entities[y][x - 1]:
                                self.world.entities[y][x - 1] = 0
                                ifdestroy = True

                            if self.world.entities[y][x + 1]:
                                self.world.entities[y][x + 1] = 0
                                ifdestroy = True

                            if self.world.entities[y + 1][x]:
                                self.world.entities[y + 1][x] = 0
                                ifdestroy = True

                            if self.world.entities[y - 1][x]:
                                self.world.entities[y - 1][x] = 0
                                ifdestroy = True

                            if self.world.entities[y][x]:
                                self.world.entities[y][x] = 0
                                ifdestroy = True

                            if ifdestroy:
                                self.world.render()
                                entities_destroy.play()
                                entities_group.update()
                                ifdestroy = False

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
                self.check_cows()

                animal_group.update()
                all_sprites.update()

                inventory_group.draw(screen)
            pg.display.flip()
        open_Menu()


class TileMap:
    def __init__(self):
        self.w = 66
        self.h = 66
        self.board = [[0] * self.w for _ in range(self.h)]
        self.entities = [[0] * self.w for _ in range(self.h)]
        self.generation()
        self.cell_size = 64
        self.entities_enabled = False

    def set_view(self, cell_size):
        self.cell_size = cell_size

    def generation(self):
        for j in range(self.h):
            for i in range(self.w):
                b = random.randint(0, 100)
                if b < 65:
                    self.board[j][i] = 0
                elif 65 <= b < 80:
                    self.board[j][i] = 1
                else:
                    self.board[j][i] = 2
        for i in range(self.w):
            self.board[0][i] = -1
            self.board[-1][i] = -1
        for i in range(self.h):
            self.board[i][0] = -1
            self.board[i][-1] = -1

    def render(self):
        tiles_group.empty()
        entities_group.empty()
        for i in range(self.w):
            for j in range(self.h):
                if self.board[j][i] == -1:
                    Tile('empty', i, j)

                    if self.entities[j][i] != 0:
                        self.entities[j][i] = 0

                if self.board[j][i] == 0:
                    Tile('grass', i, j)
                    if not self.entities_enabled:
                        b = random.randint(0, 100)
                        if b < 40:
                            self.entities[j][i] = 1
                        elif 45 > b >= 40:
                            self.entities[j][i] = 2
                        elif 60 > b >= 50:
                            self.entities[j][i] = 3

                if self.board[j][i] == 1:
                    Tile('sand', i, j)
                    if not self.entities_enabled:
                        b = random.randint(0, 100)
                        if b < 4:
                            self.entities[j][i] = 4

                if self.board[j][i] == 2:
                    Tile('stone', i, j)
                    if not self.entities_enabled:
                        b = random.randint(0, 100)
                        if b < 11:
                            self.entities[j][i] = 4

                if self.entities[j][i] == 1:
                    Entity('green', i, j)
                if self.entities[j][i] == 2:
                    Entity('flowers', i, j)
                if self.entities[j][i] == 3:
                    Entity('bush', i, j)
                if self.entities[j][i] == 4:
                    Entity('rock', i, j)

        self.entities_enabled = True

    def get_click(self, mouse_pos):
        cell = self.get_tile(mouse_pos)
        self.tile_click(cell)

    def get_tile(self, mouse_pos):
        x = mouse_pos[0] // self.cell_size
        y = mouse_pos[1] // self.cell_size
        return x, y

    def tile_click(self, cell):
        if self.board[cell[1]][cell[0]] < 1:
            self.board[cell[1]][cell[0]] += 1
        else:
            self.board[cell[1]][cell[0]] = 0


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.camera = pg.Rect(0, 0, 4224, 4224)

        self.width = 4224
        self.height = 4224

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        return obj.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x - target.rect.w + int(640 // 2)
        y = -target.rect.y - target.rect.h + int(512 // 2)

        x = min(0, x)  # ограничение на левый край
        y = min(0, y)  # ограничение на верхний край
        x = max(-(self.width - 640), x)  # на правый край
        y = max(-(self.height - 512), y)  # на нижний

        self.camera = pg.Rect(x, y, self.width, self.height)


class Tile(pg.sprite.Sprite):
    def __init__(self, types, x, y):
        super().__init__(tiles_group)
        self.cell_size = 64
        self.type = types
        self.image = tile_images[types]
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))
        self.rect = self.image.get_rect().move(self.cell_size * x,
                                               self.cell_size * y)


class Entity(pg.sprite.Sprite):
    def __init__(self, types, x, y):
        super().__init__(entities_group)
        self.cell_size = 64
        self.image = entity_images[types]
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))
        self.rect = self.image.get_rect().move(self.cell_size * x,
                                               self.cell_size * y)

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.kill()

    def get_out(self, tile):
        if self.rect.collidepoint(tile.rect.topleft):
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self, group, game, x, y, cell_size, gender):
        super().__init__(group)
        self.game = game
        self.state = "stay"
        self.tmpstate = False
        self.frames = []
        self.cur_frame = 0
        self.mirrored = False
        self.gender = gender

        if self.gender == "male":
            self.cut_sheet(load_image("p_sheet.png"))
        else:
            self.cut_sheet(load_image("f_sheet.png"))

        self.image = self.frames[self.cur_frame]
        self.size = self.image.get_size()

        self.rect = self.image.get_rect()
        self.cell_size = cell_size

        self.speed = 150

        self.vx = 0
        self.vy = 0

        self.timer = 0
        self.x = x * cell_size
        self.y = y * cell_size

        self.left = pg.transform.flip(self.image, False, False)
        self.right = pg.transform.flip(self.image, True, False)

    def comparestates(self):
        if self.tmpstate != self.state:
            self.frames.clear()
            self.tmpstate = self.state

    def cut_sheet(self, sheet):
        self.comparestates()
        self.rect = pg.Rect(0, 0, sheet.get_width() // 6,
                            sheet.get_height() // 2)

        if self.state == "run":
            for j in range(1, 2):
                for i in range(6):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pg.Rect(
                        frame_location, self.rect.size)))

            self.frames = self.frames[0:6]

        if self.state == "stay":
            for j in range(0, 1):
                for i in range(2):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pg.Rect(
                        frame_location, self.rect.size)))

            self.frames = self.frames[0:2]

    def key_movement(self):
        self.vx = 0
        self.vy = 0
        keys = pg.key.get_pressed()

        if self.x > self.game.step * 64:
            if keys[pg.K_a]:
                self.vx = -self.speed
                walk_sound.play()
        else:
            self.vx += 72  # для более плавного перехода от границы

        if self.x < (65 - self.game.step) * 64:
            if keys[pg.K_d]:
                self.vx = self.speed
                walk_sound.play()
        else:
            self.vx -= 72

        if self.y > self.game.step * 64:
            if keys[pg.K_w]:
                self.vy = -self.speed
                walk_sound.play()
        else:
            self.vy += 72

        if self.y < (65 - self.game.step) * 64:
            if keys[pg.K_s]:
                self.vy = self.speed
                walk_sound.play()
        else:
            self.vy -= 72

        if self.vx == self.vy == 0:
            self.state = "stay"
        else:
            self.state = "run"

    def update(self):
        self.timer += self.game.dt

        if self.state == "stay":
            if self.timer > 0.5:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.timer = 0

        if self.state == "run":
            if self.timer > 0.05:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.timer = 0
        self.image = pg.transform.scale(self.image,
                                        (int(self.size[0] * 4),
                                         int(self.size[1] * 4)))
        self.key_movement()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y


class Inventory:
    def __init__(self):
        self.w = 3
        self.inv = [[0] * self.w for _ in range(2)]

    def render(self):
        for i in range(self.w):
            for j in range(1):
                if self.inv[j][i] == 0:
                    Inventory_Tile('gold', i)


class Inventory_Tile(pg.sprite.Sprite):
    def __init__(self, types, x):
        super().__init__(inventory_group)
        self.cell_size = 72
        self.image = inventory_images[types]
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))
        self.rect = self.image.get_rect().move(self.cell_size * x + 360, 0)


class Drop(pg.sprite.Sprite):
    def __init__(self, types, player, x, y):
        super().__init__(drop_group)
        self.type = type
        self.cell_size = 64
        self.image = drop_images[types]
        self.image = pg.transform.scale(self.image,
                                        (self.cell_size, self.cell_size))

        self.rect = self.image.get_rect().move(self.cell_size * x,
                                               self.cell_size * y)
        self.player = player


class Cow(pg.sprite.Sprite):
    def __init__(self, group, game, x, y, cell_size):
        super().__init__(group)
        self.game = game
        self.state = "stay"
        self.tmpstate = False

        self.frames = []
        self.cur_frame = 0

        self.cut_sheet(load_image("c_sheet.png"))

        self.image = self.frames[self.cur_frame]
        self.size = self.image.get_size()

        self.rect = self.image.get_rect()
        self.cell_size = cell_size

        self.speed = 100

        self.vx = 0
        self.vy = 0

        self.timer = 0
        self.timer_choose_animation = 0

        self.x = x * cell_size
        self.y = y * cell_size

        self.movement(random.randint(0, 4))

    def comparestates(self):
        if self.tmpstate != self.state:
            self.frames.clear()
            self.tmpstate = self.state

    def cut_sheet(self, sheet):
        self.comparestates()

        self.rect = pg.Rect(0, 0, sheet.get_width() // 2,
                            sheet.get_height() // 2)

        if self.state == "run":
            for j in range(1, 2):
                for i in range(2):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pg.Rect(frame_location,
                                                                self.rect.size)))

        if self.state == "stay":
            for j in range(0, 1):
                for i in range(2):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pg.Rect(frame_location,
                                                                self.rect.size)))

        self.frames = self.frames[0:2]

    def movement(self, b):
        self.vx = 0
        self.vy = 0

        if b == 0:
            self.vx = 0
            self.vy = 0
            self.state = "stay"
            self.cut_sheet(load_image("c_sheet.png"))

        if b == 1:
            self.vx = -self.speed

        if b == 2:
            self.vx = self.speed

        if b == 3:
            self.vy = -self.speed

        if b == 4:
            self.vy = self.speed

        if b > 0:
            self.state = "run"
            self.cut_sheet(load_image("c_sheet.png"))

    def update(self):
        self.timer += self.game.dt
        self.timer_choose_animation += self.game.dt

        if self.state == "stay":
            if self.timer > 1:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.timer = 0

        if self.state == "run":
            if self.timer > 0.3:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.timer = 0

        self.image = pg.transform.scale(self.image,
                                        (int(self.size[0] * 4),
                                         int(self.size[1] * 4)))

        if self.timer_choose_animation > 2:
            self.timer_choose_animation = 0
            self.movement(random.randint(0, 4))

        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y


def open_Menu():
    men = Menu()
    men.run()


def quit():
    pg.quit()
    sys.exit()


open_Menu()