from pico2d import *
import random

Tile = [[0 for col in range(1001)] for row in range(1001)]

def fill_tile(x, y, x_size, y_size):
    x_len = int(x_size / 2)
    x_min = x - x_len
    x_max = x + x_len

    y_len = int(y_size / 2)
    y_min = y - y_len
    y_max = y + y_len
    for i in range(y_min, y_max+1):
        for j in range(x_min, x_max+1):
            Tile[i][j] = 1


class Back:
    def __init__(self):
        self.image = load_image('background.png')

    def draw(self):
        self.image.draw(400,300)


class Floor:
    def __init__(self):
        self.image = load_image('floor.png')
        self.x = 400
        self.y = 30
        self.x_size = 800

    def draw(self):
        self.image.clip_draw(0, 0, self.x_size, 60, self.x, self.y)

FLOOR_HEIGHT = 60
ENEMY_HEIGHT = 56
# Mario object
class Enemy:
    def __init__(self):
        self.image = load_image('enemy.png')
        self.x, self.y = random.randint(100,600), 76
        self.vel = -10
        self.frame = 0

    def loc_y(self, y, y_size):
        self.y = y + y_size/2 + ENEMY_HEIGHT/2 - 10

    def update(self, x, x_size):
        self.x += self.vel
        x_min = x - x_size/2
        x_max = x + x_size/2
        if self.x < x_min: # 사물 끝으로 가면 방향이 바뀜
            self.x = x_min
            self.vel = 10
        elif self.x > x_max:
            self.x = x_max
            self.vel = -10
        self.frame = (self.frame+1) % 2

    def draw(self):
        self.image.clip_draw(self.frame * 29, 0, 29, 28, self.x, self.y, 58, 56)




def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

open_canvas()

back = Back()
floors = [Floor() for i in range(3)]
floors[1].x, floors[1].y, floors[1].x_size = 400, 30, 800
floors[0].x, floors[0].y, floors[0].x_size = 600, 90, 400
floors[2].x, floors[2].y, floors[2].x_size = 700, 150, 200
enemys = [Enemy() for i in range(3)]
enemys[0].x = 200
enemys[1].x = 500
enemys[2].x = 700
for i in range(3):
    enemys[i].loc_y(floors[i].y,FLOOR_HEIGHT)
running = True


while running:
    handle_events()

    # game logic
    for i in range(3):
        enemys[i].update(floors[i].x,floors[i].x_size)


    # game drawing
    clear_canvas()
    back.draw()
    for floor in floors:
        floor.draw()
    for enemy in enemys:
        enemy.draw()
    update_canvas()
    delay(0.05)


# finalization code
close_canvas()
