from pico2d import *

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
MARIO_HEIGHT = 51
# Mario object
class Mario:
    def __init__(self):
        self.image = load_image('mario.png')
        self.x, self.y = 50, 87
        self.right_vel = 0
        self.left_vel = 0
        self.dir = 0  # 0 - right / 1 - left
        self.state = 0  # 0 - stop / 1 - move / 2 - jump
        self.frame = 0
        self.jump_vel = 0

    def move_right(self):
        if self.right_vel < 20:
            self.right_vel += 5
        self.x += self.right_vel
        self.dir = 0
        self.state = 1

    def move_left(self):
        if self.left_vel > -20:
            self.left_vel -= 5
        self.x += self.left_vel
        self.dir = 1
        self.state = 1

    def vel_reset(self):
        self.right_vel = 0
        self.left_vel = 0
        self.state = 0
        self.frame = 0

    def jump_on(self):
        if self.jump_vel == 0:
            self.jump_vel = 50
            self.y += self.jump_vel

    def falling(self):
        if self.jump_vel <= 0:
            foot = self.y - int(MARIO_HEIGHT/2)
            if Tile[foot][self.x] == 0:
                self.y += self.jump_vel
                self.jump_vel -= 10
                self.state = 2
                foot = self.y - int(MARIO_HEIGHT / 2)
                if Tile[foot][self.x] == 1 or foot < 0:
                    for i in range(foot + 1, 600):
                        if Tile[i][self.x] == 0:
                            self.y = i - 1 + int(MARIO_HEIGHT/2)
                            break
                    self.jump_vel = 0
                    self.state = 0
        else:
            self.y += self.jump_vel
            self.jump_vel -= 10
            self.state = 2


    def update(self):
        self.frame = (self.frame+1)%3


    def draw(self):
        if self.state == 1 and self.dir == 0:
            self.image.clip_draw(31 * (7+self.frame), 0, 31, 17, self.x, self.y, 123, MARIO_HEIGHT)
        elif self.state == 0 and self.dir == 0:
            self.image.clip_draw(31 * 6, 0, 31, 17, self.x, self.y, 123, MARIO_HEIGHT)
        elif self.state == 1 and self.dir == 1:
            self.image.clip_draw(31 * (4-self.frame), 0, 31, 17, self.x, self.y, 123, MARIO_HEIGHT)
        elif self.state == 0 and self.dir == 1:
            self.image.clip_draw(31 * 5, 0, 31, 17, self.x, self.y, 123, MARIO_HEIGHT)
        elif self.state == 2 and self.dir == 0:
            self.image.clip_draw(31 * 11, 0, 31, 17, self.x, self.y, 123, MARIO_HEIGHT)
        elif self.state == 2 and self.dir == 1:
            self.image.clip_draw(0, 0, 31, 17, self.x, self.y, 123, MARIO_HEIGHT)





def handle_events():
    global mario
    global running, run_right, run_left, jump_key_down
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            run_right = True
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            run_left = True
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            run_right = False
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            run_left = False

        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            mario.jump_on()



open_canvas()
back = Back()

floors = [Floor() for i in range(3)]
floors[1].x, floors[1].y, floors[1].x_size = 400, 30, 800
floors[0].x, floors[0].y, floors[0].x_size = 600, 90, 400
floors[2].x, floors[2].y, floors[2].x_size = 700, 150, 200

mario = Mario()
running = True
run_right = False
run_left = False
jump_key_down = False

for floor in floors:
    fill_tile(floor.x, floor.y, floor.x_size, FLOOR_HEIGHT)

while running:
    handle_events()

    # game logic
    if run_right:
        mario.move_right()
    elif run_left:
        mario.move_left()
    else :
        mario.vel_reset()



    mario.falling()
    mario.update()

    # game drawing
    clear_canvas()
    back.draw()
    for floor in floors:
        floor.draw()
    mario.draw()
    update_canvas()
    delay(0.05)


# finalization code
close_canvas()
