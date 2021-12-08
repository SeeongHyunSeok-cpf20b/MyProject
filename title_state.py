import game_framework
from pico2d import *
import main_state

name = "TitleState"
image = None


def enter():
    global image
    image = load_image('title.png')

    global bgm
    bgm = load_music('title.mp3')
    bgm.set_volume(90)
    bgm.play()


def exit():
    global image
    del (image)
    global bgm
    del (bgm)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()







def update():
    pass


def pause():
    pass


def resume():
    pass






