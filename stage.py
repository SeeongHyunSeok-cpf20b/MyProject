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
