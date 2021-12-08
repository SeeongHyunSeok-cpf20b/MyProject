import game_framework
from pico2d import *

import game_world
import server
import collision

import title_state


# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 60.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

JUMP_SPEED_KMPH = 80.0  # Km / Hour
JUMP_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) * 3

GRAVITY_MPS = 0.7
GRAVITY_PPS = (GRAVITY_MPS * PIXEL_PER_METER)

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, X_DOWN = range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x) : X_DOWN,
}

# Boy Action Speed
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

FLOOR_HEIGHT = 60
MARIO_HEIGHT = 40
MARIO_WIDTH = 80
# Boy States
class IdleState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

    def exit(mario, event):
        if event == X_DOWN and mario.falling== False:
            mario.jump()

    def do(mario):
        pass

    def draw(mario):
        cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
        if mario.dead:
            mario.dead_image.draw(cx,cy)
        else:
            if mario.falling:
                if mario.dir == 1:
                    mario.image.clip_draw(31 * 11, 0, 31, 17, cx, cy, MARIO_WIDTH, MARIO_HEIGHT)
                else:
                    mario.image.clip_draw(0, 0, 31, 17, cx, cy, MARIO_WIDTH, MARIO_HEIGHT)
            else:
                if mario.dir == 1:
                    mario.image.clip_draw(31 * 6, 0, 31, 17, cx, cy, MARIO_WIDTH, MARIO_HEIGHT)
                else:
                    mario.image.clip_draw(31 * 5, 0, 31, 17, cx, cy, MARIO_WIDTH, MARIO_HEIGHT)

class RunState:
    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS
        mario.dir = clamp(-1, mario.velocity, 1)

    def exit(mario, event):
        if event == X_DOWN and mario.falling == False:
            mario.jump()

    def do(mario):
        # boy.frame = (boy.frame + 1) % 8
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

        mario.x += mario.velocity * game_framework.frame_time

        if mario.dir == 1:
            if (collision.collide_side(mario.x, mario.y - MARIO_HEIGHT/2 + 10, server.stage1_1)):
                temp_x = ((mario.x / 40) - 1) * 40
                mario.x = temp_x - 12
        else :
            if (collision.collide_side(mario.x, mario.y - MARIO_HEIGHT / 2 + 10, server.stage1_1)):
                temp_x = (mario.x / 40) * 40
                mario.x = temp_x + 15 + 2


    def draw(mario):
        cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
        if mario.dead:
            mario.dead_image.draw(cx,cy)
        else:
            if mario.falling:
                if mario.dir == 1:
                    mario.image.clip_draw(31 * 11, 0, 31, 17, cx, cy, MARIO_WIDTH, MARIO_HEIGHT)
                else:
                    mario.image.clip_draw(0, 0, 31, 17, cx, cy, MARIO_WIDTH, MARIO_HEIGHT)
            else:
                if mario.dir == 1:
                    mario.image.clip_draw(31 * int(7+mario.frame), 0, 31, 17, cx, cy, MARIO_WIDTH, MARIO_HEIGHT)
                else:
                    mario.image.clip_draw(31 * int(4-mario.frame), 0, 31, 17, cx, cy, MARIO_WIDTH, MARIO_HEIGHT)




next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, X_DOWN: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, X_DOWN: RunState},
}


# Mario object
class Mario:
    def __init__(self):
        self.image = load_image('mario.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.end_image = load_image('win.png')
        self.dead_image = load_image('dead.png')
        self.x, self.y = 50, 100
        self.falling = False
        self.velocity = 0
        self.jump_velocity = 0
        self.dir = 1  # 0 - right / 1 - left
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.frame = 0
        self.jump_velocity = 0
        self.end = False
        self.win = False
        self.dead = False

        self.jump_bgm = load_music('jump.mp3')

        self.clear_bgm = load_music('clear.wav')

        self.coin_bgm = load_music('coin.mp3')

        self.dead_bgm = load_music('dead.mp3')


        self.stomp_bgm = load_music('stomp.wav')


        self.fall = GRAVITY_MPS
        self.d = 0

        self.start_time = 0
        self.end_time = 0


    def get_bb(self):
        # fill here
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 15, cy - MARIO_HEIGHT/2, cx + 12, cy + MARIO_HEIGHT/2

    def jump(self):
        self.jump_bgm.set_volume(32)
        self.jump_bgm.play(1)
        self.falling = True
        self.jump_velocity = JUMP_SPEED_PPS

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if (self.win):
            self.end_time = get_time()
            if (self.end_time - self.start_time > 6):
                game_framework.change_state(title_state)
                return

        if (self.dead):
            self.velocity = 0
            self.y+=self.fall
            self.d += self.fall
            if (self.d > 100):
                self.d = 0
                self.fall *= -1

            if self.y < 0:
                game_framework.change_state(title_state)
                return


        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        if (self.falling):
            self.y += int(self.jump_velocity * game_framework.frame_time)

            for i in range(15):
                if (collision.colide(self, server.enemy[i]) and server.enemy[i].live and self.dead == False):
                    self.stomp_bgm.set_volume(100)
                    self.stomp_bgm.play(1)
                    self.jump_velocity = JUMP_SPEED_PPS / 2
                    server.enemy[i].dead()

            if (self.jump_velocity > 0 and (collision.collide_itembox(self.x-15, self.y + MARIO_HEIGHT/2 + 2, server.stage1_1)
                                      or collision.collide_itembox(self.x+15, self.y + MARIO_HEIGHT/2 + 2, server.stage1_1))):
                self.coin_bgm.set_volume(96)
                self.coin_bgm.play(1)
                self.jump_velocity = 0
                self.y -= int(self.jump_velocity * game_framework.frame_time)

            if (self.jump_velocity > 0 and (collision.collide_bottom(self.x-15, self.y + MARIO_HEIGHT/2 + 2, server.stage1_1)
                                      or collision.collide_bottom(self.x+15, self.y + MARIO_HEIGHT/2 + 2, server.stage1_1))):
                self.jump_velocity = 0
                self.y -= int(self.jump_velocity * game_framework.frame_time)

            self.jump_velocity -= GRAVITY_PPS

            if (self.y < 0):
                self.dead_bgm.set_volume(90)
                self.dead_bgm.play(1)
                self.dead = True




        if (self.jump_velocity <= 0 and collision.collide_bottom(self.x-15, self.y - MARIO_HEIGHT/2 - 2, server.stage1_1)
                or collision.collide_bottom(self.x+12, self.y - MARIO_HEIGHT/2 - 2, server.stage1_1)):
            self.falling = False
            self.jump_velocity = 0
        else:
            self.falling = True

        for i in range(15):
            if (collision.colide(self, server.enemy[i]) and server.enemy[i].live):
                self.dead_bgm.set_volume(64)
                self.dead_bgm.play(1)
                self.dead = True
                break

        if (collision.collide_end(self.x, self.y, server.stage1_1)):
            self.clear_bgm.set_volume(90)
            self.clear_bgm.play(1)
            self.end = True;
            self.start_time = get_time()



        self.x = clamp(0, self.x, server.background.w - 1)
        self.y = clamp(0, self.y, server.background.h - 1)

    def draw(self):

        self.cur_state.draw(self)
        # cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        # self.font.draw(cx - 60, cy + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))
        # draw_rectangle(*self.get_bb())
        # debug_print(str(self.y) +'Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir) + ' Frame Time:' + str(
        #     game_framework.frame_time) )

        if (self.end):
            self.end_image.draw(400, 300)
            self.win =True


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
    """def move_right(self):
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
            self.image.clip_draw(0, 0, 31, 17, self.x, self.y, 123, MARIO_HEIGHT)"""

