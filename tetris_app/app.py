#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Very simple tetris implementation
#
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# NOTE: If you're looking for the old python2 version, see
#       <https://gist.github.com/silvasur/565419/45a3ded61b993d1dd195a8a8688e7dc196b08de8>

# Copyright (c) 2010 "Laria Carolin Chabowski"<me@laria.me>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pygame
import sys

import common
from tetris import Tetris


class App(object):
    def __init__(self, rows=22, cols=10, scale=1, slow=True, display=True, manual=True):
        self.display = display
        self.slow = slow
        self.game = Tetris(rows, cols)
        self.manual = True

        if manual and not display:
            print("Display disabled but manual control enabled. Modify the parameters with which the app"
                  "is instantiated to change this.", file=sys.stderr)

        if self.display:
            self.line_height = common.line_height * scale
            self.text_size = common.text_size * scale
            self.cell_size = common.cell_size * scale
            self.width = self.cell_size * (cols + 6)
            self.height = self.cell_size * rows
            self.rlim = self.cell_size * cols

            pygame.init()
            pygame.key.set_repeat(250, 25)

            self.bground_grid = [[8 if x % 2 == y % 2 else 0 for x in range(cols)] for y in range(rows)]

            self.default_font = pygame.font.Font(
                pygame.font.get_default_font(), self.text_size)

            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.event.set_blocked(pygame.MOUSEMOTION)  # block mouse events, not needed

            self.paused = False

            pygame.time.set_timer(pygame.USEREVENT + 1, self.game.delay)

    def display_msg(self, msg, top_left):
        x, y = top_left
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255, 255, 255),
                    (0, 0, 0)),
                (x, y))
            y += self.line_height

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = self.default_font.render(line, False,
                                                 (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
                self.width // 2 - msgim_center_x,
                self.height // 2 - msgim_center_y + i * 22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        common.colors[val],
                        pygame.Rect(
                            (off_x + x) *
                            self.cell_size,
                            (off_y + y) *
                            self.cell_size,
                            self.cell_size,
                            self.cell_size), 0)

    def quit(self):
        self.screen.fill((0, 0, 0))
        self.center_msg("Exiting...")
        pygame.display.update()

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_slow(self):
        self.slow = not self.slow

    def start_game(self):
        if self.game.game_over:
            rows, cols = self.game.rows, self.game.cols
            self.game = Tetris(rows, cols)  # new instance
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # reset timer

    def run(self):
        key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.game.move(-1),
            'RIGHT': lambda: self.game.move(+1),
            'DOWN': lambda: self.game.drop(True),
            'UP': self.game.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game,
            'RETURN': self.game.instant_drop,
            'q': lambda: self.quit(),
            's': self.toggle_slow
        }
        clock = None
        if self.display:
            clock = pygame.time.Clock()
        while 1:
            if self.display:
                self.screen.fill((0, 0, 0))
                if self.game.game_over:
                    self.center_msg(""" Game Over!\nYour score: %d
                                        Press space to continue""" % self.game.score)
                else:
                    if self.paused:
                        self.center_msg("Paused")
                    else:
                        pygame.draw.line(self.screen,
                                         (255, 255, 255),
                                         (self.rlim + 1, 0),
                                         (self.rlim + 1, self.height - 1))
                        self.display_msg("Next:", (
                            self.rlim + self.cell_size,
                            2))
                        self.display_msg(" Score: %d\n\nLevel: %d\
                                        \nLines: %d" % (self.game.score, self.game.level, self.game.lines),
                                         (self.rlim + self.cell_size, self.cell_size * 5))
                        self.draw_matrix(self.bground_grid, (0, 0))
                        self.draw_matrix(self.game.board, (0, 0))
                        self.draw_matrix(self.game.stone,
                                         (self.game.stone_x, self.game.stone_y))
                        self.draw_matrix(self.game.next_stone,
                                         (self.game.cols + 1, 2))
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return self.quit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.toggle_pause()

                    elif not self.paused:
                        if event.type == pygame.USEREVENT + 1:
                            if self.slow:
                                self.game.drop(manual=False)
                                pygame.time.set_timer(pygame.USEREVENT + 1, self.game.delay)
                        elif event.type == pygame.KEYDOWN:
                            for key in key_actions:
                                if event.key == eval("pygame.K_" + key):
                                    key_actions[key]()

            if self.slow:
                clock.tick(common.maxfps)
            else:
                self.game.drop(manual=False)


if __name__ == '__main__':
    app = App(scale=2)
    app.run()
