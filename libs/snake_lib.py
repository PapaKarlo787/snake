from random import randint
from threading import Timer
from level_lib import Level


class Location:
    RIGHT = "RIGHT"
    UP = "UP"
    LEFT = "LEFT"
    DOWN = "DOWN"


class Object:
    VOID = "VOID"
    HEAD = "HEAD"
    SCORE = "SCORE"
    CLOCK = "CLOCK"
    HEART = "HEART"
    BLOOD = "BLOOD"
    WALL = "WALL"
    TAIL = "TAIL"
    APPLE = "APPLE"
    POISON = "POISON"
    VERTICAL = "VERTICAL"
    HORISONTAL = "HORISONTAL"


class Snake:
    def __init__(self, sound, w, h, fn, config, is_lev):
        self.fn = fn
        try:
            self.load_level(Level(fn, w, h))
            self.error = None
        except Exception as e:
            self.error = str(e)
            self.load_standart_level(w, h)
        self.create_level()
        self.load_config(config)
        self.score = 0
        self.lev = is_lev
        self.ring = lambda num, n: (n + num) % n
        self.hp = 2
        self.queue_timers = []
        self.loc = Location.RIGHT
        self.prev_loc = self.loc
        self.hungry = True
        self.killed = False
        self.paused = False
        self.timeout = False
        self.cant_turn = False
        self.sounds = sound
        self.food = [Object.APPLE, Object.POISON]
        self.drop_apple()
        self.sounds.back.play()

    def create_level(self):
        self.mem = [((0, 0), Object.VOID)] * self.h * self.w
        beg_cond = ["{}_{}".format(Object.TAIL, Location.RIGHT),
                    Object.HORISONTAL,
                    "{}_{}".format(Object.HEAD, Location.RIGHT)]
        for i in range(3):
            self.map[0][i] = beg_cond[i]
            self.mem[i] = ((i, 0), beg_cond[i])

    def load_standart_level(self, w, h):
        self.h = h
        self.w = w
        self.timer = 10
        self.map = [0] * self.h
        for i in range(h):
            self.map[i] = [Object.VOID] * w

    def load_level(self, level):
        self.h = level.h
        self.w = level.w
        self.timer = level.timer
        self.map = level.map

    def load_config(self, config):
        self.poisons = config['poisons']
        self.maxpoisons = config['maxpoisons']
        self.delay = config['delay']
        self.lives = config['lives']

    def down(self):
        if not (self.loc == Location.UP or self.cant_turn):
            self.set_loc(Location.DOWN)

    def up(self):
        if not (self.loc == Location.DOWN or self.cant_turn):
            self.set_loc(Location.UP)

    def left(self):
        if not (self.loc == Location.RIGHT or self.cant_turn):
            self.set_loc(Location.LEFT)

    def right(self):
        if not (self.loc == Location.LEFT or self.cant_turn):
            self.set_loc(Location.RIGHT)

    def start_pause(self):
        self.paused = not self.paused

    def set_loc(self, loc):
        if self.paused:
            return
        self.cant_turn = True
        self.loc = loc

    def shoot(self):
        if self.paused:
            return
        self.cant_turn = True
        if self.poisons == 0:
            return
        directions = {"{}_{}".format(Object.HEAD, Location.DOWN): (0, 1),
                      "{}_{}".format(Object.HEAD, Location.LEFT): (-1, 0),
                      "{}_{}".format(Object.HEAD, Location.RIGHT): (1, 0),
                      "{}_{}".format(Object.HEAD, Location.UP): (0, -1)}
        x, y = self.mem[self.hp][0]
        dx, dy = directions[self.map[y][x]]
        self.poisons -= 1
        while self.map[y][x] == Object.VOID or Object.HEAD in self.map[y][x]:
            x = self.ring(x+dx, self.w)
            y = self.ring(y+dy, self.h)
        if self.map[y][x] == Object.WALL:
            self.map[y][x] = Object.VOID
            self.sounds.boom.play()
            self.init_rollback(x, y)
        elif self.map[y][x] in self.food:
            self.sounds.waste.play()
            self.map[y][x] = Object.VOID
            self.drop_apple()

    def set_wall_back(self, x, y):
        if not self.map[y][x] == Object.VOID or self.paused:
            self.init_rollback(x, y)
        else:
            self.map[y][x] = Object.WALL

    def init_rollback(self, x, y):
        delay = randint(3, 8)
        self.queue_timers.append(Timer(delay, self.set_wall_back, (x, y)))
        self.queue_timers[-1].start()

    def reset_tail(self):
        if self.hungry:
            x, y = self.mem[0][0]
            self.map[y][x] = Object.VOID
            self.mem = self.mem[1:] + self.mem[:1]
            self.set_tail()
        else:
            self.hp += 1

    def move(self):
        if self.paused:
            return
        if self.lev:
            self.timer -= self.delay/1000
        self.timeout = self.timer <= 0
        if self.timeout:
            self.sounds.clock.play()
        if not self.sounds.back.is_playing():
            self.sounds.back.play()
        x, y = self.mem[self.hp][0]
        self.reset_tail()
        self.cant_turn = False
        self.hungry = True
        self.map[y][x] = self.get_body()
        self.mem[self.hp-1] = ((x, y), self.map[y][x])
        x, y = self.sel_loc(x, y)
        result = self.check_for_eaten_object(self.map[y][x])
        self.map[y][x] = "{}_{}".format(Object.HEAD, self.loc)
        self.mem[self.hp] = ((x, y), self.map[y][x])
        self.prev_loc = self.loc

    def get_body(self):
        if not self.loc == self.prev_loc:
            if self.prev_loc in [Location.DOWN, Location.UP]:
                return self.get_angle(self.prev_loc)
            if self.prev_loc == Location.LEFT:
                return self.get_angle(Location.RIGHT)
            return self.get_angle(Location.LEFT)
        if self.loc == Location.RIGHT or self.loc == Location.LEFT:
            return Object.HORISONTAL
        return Object.VERTICAL

    def set_tail(self):
        x, y = self.mem[0][0]
        nx, ny = self.mem[1][0]
        checks = {self.ring(x - nx, self.w): Location.LEFT,
                  self.ring(nx - x, self.w): Location.RIGHT,
                  self.ring(ny - y, self.h): Location.DOWN,
                  self.ring(y - ny, self.h): Location.UP}
        for value in checks:
            if value == 1:
                self.map[y][x] = "{}_{}".format(Object.TAIL, checks[value])
                self.mem[0] = ((x, y), self.map[y][x])

    def get_angle(self, prev_loc):
        if self.loc in [Location.LEFT, Location.RIGHT]:
            return "{}-{}".format(prev_loc, self.loc)
        if self.loc == Location.DOWN:
            return "{}-{}".format(Location.UP, prev_loc)
        return "{}-{}".format(Location.DOWN, prev_loc)

    def check_for_eaten_object(self, prev):
        if prev == Object.APPLE:
            self.sounds.nyam.play()
            self.score += 1
            self.hungry = False
            self.drop_apple()
        elif prev == Object.POISON:
            self.poisons += 1
            self.score += 0.5
            self.sounds.drink.play()
            self.drop_apple()
        elif not prev == Object.VOID:
            self.sounds.dead.play()
            self.lives -= 1
            if not self.lives:
                self.killed = True

    def faster(self):
        if self.paused:
            return
        if self.delay - 50 > 0:
            self.delay -= 50

    def slower(self):
        if self.paused:
            return
        if self.delay + 50 < 1000:
            self.delay += 50

    def sel_loc(self, x, y):
        if self.loc == Location.DOWN:
            y = self.ring(y+1, self.h)
        elif self.loc == Location.UP:
            y = self.ring(y-1, self.h)
        elif self.loc == Location.RIGHT:
            x = self.ring(x+1, self.w)
        elif self.loc == Location.LEFT:
            x = self.ring(x-1, self.w)
        return (x, y)

    def drop_apple(self):
        while True:
            x = randint(0, self.w-1)
            y = randint(0, self.h-1)
            if self.map[y][x] == Object.VOID:
                break
        if randint(0, 5) == 5 and self.poisons < self.maxpoisons:
            self.map[y][x] = Object.POISON
        else:
            self.map[y][x] = Object.APPLE
