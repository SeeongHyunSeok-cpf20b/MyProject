import random
import json
import os


from pico2d import *

import game_framework
import game_world

from mario import Mario
from enemy import Enemy

from background import FixedBackground as Background

import server


name = "MainState"


def enter():
    server.mario = Mario()
    game_world.add_object(server.mario, 1)

    server.enemy = [Enemy() for i in range(15)]

    server.background = Background()
    game_world.add_object(server.background, 0)

    y = 0
    i = 0
    for row in server.stage1_1:
        x = 0
        y += 1
        for col in row:
            x += 1
            if col == '5':
                server.stage1_1[y-1][x-1] = '-1'
                server.enemy[i].loc_y(40 * x - 20, 40 * (15 - y + 1) - 20)
                i+=1

    for j in range(15):
        game_world.add_object(server.enemy[j], 1)




def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()





