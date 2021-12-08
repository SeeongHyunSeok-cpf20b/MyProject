import game_framework
from pico2d import *

import game_world
import random
import collision
import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

FALL_SPEED_KMPH = 20.0  # Km / Hour
FALL_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
FALL_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
FALL_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

FLOOR_HEIGHT = 60
ENEMY_HEIGHT = 56
# Mario object
class Enemy:
    def __init__(self):
        self.image = load_image('enemy.png')
        self.x, self.y = 0, 0
        self.vel = -RUN_SPEED_PPS * game_framework.frame_time
        self.frame = 0
        self.live = True
        self.fall = -RUN_SPEED_PPS * game_framework.frame_time
    def loc_y(self, x, y):
        self.x = x
        self.y = y

    def get_bb(self):
        # fill here
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 20, cy - 20, cx + 20, cy + 20

    def update(self):
        if (self.live):
            self.x += self.vel
            if collision.check_bottom(self.x - 20 - 2, self.y - 20 - 2, server.stage1_1):
                self.x -= self.vel
                self.vel = RUN_SPEED_PPS * game_framework.frame_time
            elif collision.check_bottom(self.x + 20 + 2, self.y - 20 - 2, server.stage1_1):
                self.x += self.vel
                self.vel = -RUN_SPEED_PPS * game_framework.frame_time

            if self.vel >= 0:
                if (collision.collide_side(self.x, self.y - 20 + 10, server.stage1_1)):
                    temp_x = ((self.x / 40) - 1) * 40
                    self.x = temp_x + 12
                    self.vel = -RUN_SPEED_PPS * game_framework.frame_time
            else :
                if (collision.collide_side(self.x, self.y - 20 + 10 / 2 + 10, server.stage1_1)):
                    temp_x = (self.x / 40) * 40
                    self.x = temp_x + 15 + 2
                    self.vel = RUN_SPEED_PPS * game_framework.frame_time
            self.frame = (self.frame+1) % 2
        else:
            self.y += self.fall
            if (self.y < -40):
                self.fall = 0

    def draw(self):
        cx, cy = self.x - server.background.window_left , self.y - server.background.window_bottom

        self.image.clip_draw(self.frame * 29, 0, 29, 28, cx, cy, 60, 60)


    def dead(self):
        self.vel = 0
        self.live = False


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# open_canvas()
#
# back = Back()
# floors = [Floor() for i in range(3)]
# floors[1].x, floors[1].y, floors[1].x_size = 400, 30, 800
# floors[0].x, floors[0].y, floors[0].x_size = 600, 90, 400
# floors[2].x, floors[2].y, floors[2].x_size = 700, 150, 200
# enemys = [Enemy() for i in range(3)]
# enemys[0].x = 200
# enemys[1].x = 500
# enemys[2].x = 700
# for i in range(3):
#     enemys[i].loc_y(floors[i].y,FLOOR_HEIGHT)
# running = True
#
#
# while running:
#     handle_events()
#
#     # game logic
#     for i in range(3):
#         enemys[i].update(floors[i].x,floors[i].x_size)
#
#
#     # game drawing
#     clear_canvas()
#     back.draw()
#     for floor in floors:
#         floor.draw()
#     for enemy in enemys:
#         enemy.draw()
#     update_canvas()
#     delay(0.05)
#
#
# # finalization code
# close_canvas()
