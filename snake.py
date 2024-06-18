#!/usr/bin/env python3.6


import argparse
import sys
from os.path import join, isfile, isdir
from os import listdir, path
sys.path.insert(0, path.abspath('libs'))
from snake_lib import Snake
from config_lib import Config
from sound_lib import Sound
from window_lib import Window


class SnakeGame:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--lev", type=str, help="select level")
        parser.add_argument("-c", "--conf", type=str, help="select config",
                            default="snake.conf")
        parser.add_argument("-s", "--scenario", help="select level folder",
                            type=str)
        conf_blocks = {'WINDOW': {'h': 15, 'w': 15},
                       'SNAKE': {'delay': 200, 'poisons': 5, 'maxpoisons': 20,
                                 'lives': 3}}
        self.sound = Sound()
        self.args = parser.parse_args()
        self.config = Config(self.args.conf, conf_blocks).result
        self.w = self.config['WINDOW']['w']
        self.h = self.config['WINDOW']['h']

    def run(self):
        need_continue = True
        while need_continue:
            need_continue = self.level_mode(path.abspath(self.args.scenario))\
                if self.args.scenario else self.score_mode()

    def score_mode(self):
        level = path.abspath(self.args.lev) if self.args.lev else ""
        game = Window(Snake(self.sound, self.w, self.h, level,
                            self.config['SNAKE'], False))
        self.args.lev = game.snake.fn
        for t in game.snake.queue_timers:
            t.cancel()
        if not game.snake.timeout and not game.snake.killed:
            return
        return Window.ask("Score {}. Restart?".format(game.snake.score),
                          "Score")

    def level_mode(self, folder):
        score = 0
        levels = list(filter(lambda x: isfile(join(folder, x)),
                             listdir(folder)))
        levels.sort()
        for level in levels:
            snake = Snake(self.sound, self.w, self.h, join(folder, level),
                          self.config['SNAKE'], True)
            game = Window(snake)
            score += game.snake.score + game.snake.lives * 3
            for t in game.snake.queue_timers:
                t.cancel()
            if not (game.snake.timeout or game.snake.killed):
                return
        return Window.ask("Total score {}. Restart?".format(score), "Score")


if __name__ == '__main__':
    game = SnakeGame()
    try:
        game.run()
    except Exception as e:
        print(e)
