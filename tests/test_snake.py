import unittest
from snake_lib import Snake, Location as Loc, Object as Obj
from sound_lib import Sound
from level_lib import Level


class SnakeTests(unittest.TestCase):
    def test_turning(self):
        snake = Snake(Sound(True), 5, 5, None, self.make_conf(), False)
        snake.map = [['VOID', 'VOID', 'VOID', 'VOID', 'VOID'],
                     ['VOID', 'VOID', 'VOID', 'VOID', 'VOID'],
                     ['VOID', 'VOID', 'VOID', 'VOID', 'VOID'],
                     ['VOID', 'VOID', 'VOID', 'VOID', 'VOID'],
                     ['VOID', 'VOID', 'VOID', 'VOID', 'VOID']]
        snake.move()
        snake.down()
        snake.move()
        snake.left()
        snake.move()
        snake.up()
        snake.move()
        snake.right()
        snake.move()
        head_result = ((3, 0), "{}_{}".format(Obj.HEAD, Loc.RIGHT))
        tail_result = ((2, 1), "{}_{}".format(Obj.TAIL, Loc.UP))
        self.assertEqual(snake.mem[snake.hp], head_result)
        self.assertEqual(snake.mem[0], tail_result)

    def test_eat_apple(self):
        snake = Snake(Sound(True), 5, 5, None, self.make_conf(), False)
        self.assertEqual(snake.score, 0)
        snake.map[0][3] = Obj.APPLE
        snake.move()
        head_result = ((3, 0), "{}_{}".format(Obj.HEAD, Loc.RIGHT))
        tail_result = ((1, 0), "{}_{}".format(Obj.TAIL, Loc.RIGHT))
        self.assertEqual(snake.mem[snake.hp], head_result)
        self.assertEqual(snake.mem[0], tail_result)
        self.assertEqual(snake.score, 1)

    def test_get_poison(self):
        snake = Snake(Sound(True), 5, 5, None, self.make_conf(), False)
        self.assertEqual(snake.score, 0)
        self.assertEqual(snake.poisons, 1)
        snake.map[0][3] = Obj.POISON
        snake.move()
        head_result = ((3, 0), "{}_{}".format(Obj.HEAD, Loc.RIGHT))
        tail_result = ((1, 0), "{}_{}".format(Obj.TAIL, Loc.RIGHT))
        self.assertEqual(snake.mem[snake.hp], head_result)
        self.assertEqual(snake.mem[0], tail_result)
        self.assertEqual(snake.score, 0.5)
        self.assertEqual(snake.poisons, 2)

    def test_shoot_food(self):
        snake = Snake(Sound(True), 10, 10, None, self.make_conf(poisons=3),
                      False)
        snake.map[0][3] = Obj.POISON
        snake.map[0][4] = Obj.APPLE
        snake.shoot()
        snake.shoot()
        snake.move()
        snake.move()
        head_result = ((4, 0), "{}_{}".format(Obj.HEAD, Loc.RIGHT))
        tail_result = ((2, 0), "{}_{}".format(Obj.TAIL, Loc.RIGHT))
        self.assertEqual(snake.mem[snake.hp], head_result)
        self.assertEqual(snake.mem[0], tail_result)
        self.assertEqual(snake.poisons, 1)

    def test_eat_wall(self):
        snake = Snake(Sound(True), 10, 10, None, self.make_conf(), False)
        self.assertEqual(snake.lives, 3)
        snake.map[0][3] = Obj.WALL
        snake.move()
        head_result = ((3, 0), "{}_{}".format(Obj.HEAD, Loc.RIGHT))
        tail_result = ((1, 0), "{}_{}".format(Obj.TAIL, Loc.RIGHT))
        self.assertEqual(snake.mem[snake.hp], head_result)
        self.assertEqual(snake.mem[0], tail_result)
        self.assertEqual(snake.lives, 2)

    def test_shoot_wall(self):
        snake = Snake(Sound(True), 10, 10, None, self.make_conf(), False)
        self.assertEqual(snake.lives, 3)
        snake.map[0][3] = Obj.WALL
        snake.shoot()
        snake.move()
        head_result = ((3, 0), "{}_{}".format(Obj.HEAD, Loc.RIGHT))
        tail_result = ((1, 0), "{}_{}".format(Obj.TAIL, Loc.RIGHT))
        self.assertEqual(snake.mem[snake.hp], head_result)
        self.assertEqual(snake.mem[0], tail_result)
        self.assertEqual(snake.lives, 3)
        snake.queue_timers[0].cancel()

    def test_user_level(self):
        snake = Snake(Sound(True), 10, 10, "tests/level_test_files/simple",
                      self.make_conf(), False)
        snake.down()
        snake.move()
        self.assertEqual(snake.lives, 2)

    def test_wrong_user_level(self):
        snake = Snake(Sound(True), 10, 10, "level_test_files/wrong",
                      self.make_conf(), False)

    def make_conf(self, maxp=3, poisons=1, delay=100, lives=3):
        return {'maxpoisons': maxp, 'poisons': poisons,
                'delay': delay, 'lives': lives}


if __name__ == '__main__':
    unittest.main()
