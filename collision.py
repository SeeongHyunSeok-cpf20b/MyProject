def collide_bottom(x, y, tile):
    if y < 0:
        return False
    cur = tile[14 - int(y/40)][int(x/40)]
    if cur != '-1' and cur != '4':
        return True
    else:
        return False

def collide_itembox(x, y, tile):
    if y < 0:
        return False
    cur = tile[14 - int(y/40)][int(x/40)]
    if cur == '2' or cur == '3':
        tile[14 - int(y/40)][int(x/40)] = '1'
        return True
    else:
        return False

def check_bottom(x, y, tile):
    cur = tile[14 - int(y/40)][int(x/40)]
    if cur == '-1':
        return True
    else:
        return False

def collide_side(x, y, tile):
    if y < 0:
        return False
    cur = tile[14 - int(y / 40)][int(x / 40)]
    if cur != '-1'and cur != '4':
        return True
    else:
        return False

def colide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collide_end(x, y, tile):
    cur = tile[14 - int(y / 40)][int(x / 40)]
    if cur == '4':
        return True
    else:
        return False