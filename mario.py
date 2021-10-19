from pico2d import *


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
class Mario:
    def __init__(self):
        self.image = load_image('mario.png')
        self.x, self.y = 50, 87
        self.right_vel = 0
        self.left_vel = 0
        self.dir = 0  # 0 - right / 1 - left
        self.state = 0  # 0 - stop / 1 - move / 2 - jump
        self.frame = 0
        self.jump_vel = 50
        self.jumping = False

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
        self.jumping = True



    def jump(self):
        if self.jumping:
            self.y += self.jump_vel
            self.jump_vel -= 9.8
            self.state = 2
        if self.y < 87:
            self.y = 87
            self.jump_vel = 50
            self.jumping = False
            self.state = 0

    def update(self):
        self.frame = (self.frame+1)%3

    def draw(self):
        if self.state == 1 and self.dir == 0:
            self.image.clip_draw(31 * (7+self.frame), 0, 31, 17, self.x, self.y, 123, 51)
        elif self.state == 0 and self.dir == 0:
            self.image.clip_draw(31 * 6, 0, 31, 17, self.x, self.y, 123, 51)
        elif self.state == 1 and self.dir == 1:
            self.image.clip_draw(31 * (4-self.frame), 0, 31, 17, self.x, self.y, 123, 51)
        elif self.state == 0 and self.dir == 1:
            self.image.clip_draw(31 * 5, 0, 31, 17, self.x, self.y, 123, 51)
        elif self.state == 2 and self.dir == 0:
            self.image.clip_draw(31 * 11, 0, 31, 17, self.x, self.y, 123, 51)
        elif self.state == 2 and self.dir == 1:
            self.image.clip_draw(0, 0, 31, 17, self.x, self.y, 123, 51)





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
floor = Floor()
mario = Mario()
running = True
run_right = False
run_left = False
jump_key_down = False

while running:
    handle_events()

    # game logic
    if run_right:
        mario.move_right()
    elif run_left:
        mario.move_left()
    else :
        mario.vel_reset()

    mario.jump()


    mario.update()
    # game drawing
    clear_canvas()
    back.draw()
    floor.draw()
    mario.draw()
    update_canvas()
    delay(0.05)


# finalization code
close_canvas()
