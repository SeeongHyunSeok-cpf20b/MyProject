from pico2d import *
import random


class Back:
    def __init__(self):
        self.image = load_image('background.png')

    def draw(self):
        self.image.draw(400,300)


class Floor:
    def __init__(self):
        self.image = load_image('floor.png')

    def draw(self):
        self.image.draw(400, 30)


# Mario object
class Enemy:
    def __init__(self):
        self.image = load_image('enemy.png')
        self.x, self.y = random.randint(100,600), 76
        self.vel = -10
        self.frame = 0

    def update(self):
        self.x += self.vel
        if self.x < 0: # 사물 끝으로 가면 방향이 바뀜
            self.x = 0
            self.vel = 10
        elif self.x > 800:
            self.x = 800
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
floor = Floor()
enemy = Enemy()
running = True


while running:
    handle_events()

    # game logic
    enemy.update()


    # game drawing
    clear_canvas()
    back.draw()
    floor.draw()
    enemy.draw()
    update_canvas()
    delay(0.05)


# finalization code
close_canvas()
