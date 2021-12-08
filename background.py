import random
import server


from pico2d import *

class FixedBackground:

    def __init__(self):
        self.image = load_image('1-1.png')
        self.block_image = load_image('block.png')
        self.item_block_image = load_image('item-block.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

        # self.bgm = load_music('main_bgm.mp3')
        # self.bgm.set_volume(64)
        # self.bgm.repeat_play()

        server.stage1_1 = []
        f = open('1-1.txt', 'r')
        lines = f.readlines()
        for line in lines:
            list = line.split()
            server.stage1_1.append(list)




    def draw(self):
        # fill here
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, server.background.canvas_width, server.background.canvas_height, 0, 0)
        y = 0
        for row in server.stage1_1:
            x = 0
            y += 1
            for col in row:
                x+=1
                cx, cy = 40 * x - 20 - server.background.window_left,40 * (15 - y + 1) -20 - server.background.window_bottom
                if col == '2':
                    self.item_block_image.draw(cx, cy)
                if col == '3':
                    self.item_block_image.draw(cx, cy)

                if col == '1':
                    self.block_image.draw(cx, cy)
        pass

    def update(self):
        # fill here
        self.window_left = clamp(0, int(server.mario.x) - server.background.canvas_width // 2, server.background.w - server.background.canvas_width)
        self.window_bottom = clamp(0, int(server.mario.y) - server.background.canvas_height // 2, server.background.h - server.background.canvas_height)
        pass

    def handle_event(self, event):
        pass
