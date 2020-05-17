#!/usr/bin/env python3
from random import randrange as rand

import common


class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.next_stone = common.tetris_shapes[rand(len(common.tetris_shapes))]

        self.board = self.new_board()
        self.stone, self.stone_x, self.stone_y, self.next_stone = self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        self.game_over = False
        self.delay = 1000

    def new_board(self):
        board = [
            [0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]
        board += [[1 for _ in range(self.cols)]]
        return board

    def new_stone(self):
        stone = self.next_stone[:]
        next_stone = common.tetris_shapes[rand(len(common.tetris_shapes))]
        stone_x = int(self.cols / 2 - len(stone[0]) / 2)
        stone_y = 0

        if self.check_collision(self.board, stone, (stone_x, stone_y)):
            self.game_over = True

        return stone, stone_x, stone_y, next_stone

    def rotate_stone(self):
        if not self.game_over:
            new_stone = self.rotate_clockwise(self.stone)
            if not self.check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level

    def update_level(self):
        if self.lines >= self.level * 6:
            self.level += 1

    def update_delay(self):
        new_delay = 1000 - 50 * (self.level - 1)
        if new_delay < 100:
            new_delay = 100
        self.delay = new_delay

    def drop(self, manual):
        if not self.game_over:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if self.check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.board = self.join_matrices(self.board, self.stone, (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = self.remove_row(
                                self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                if cleared_rows:
                    self.add_cl_lines(cleared_rows)
                    self.update_level()
                    self.update_delay()
                return True
        return False

    def move(self, delta_x):
        if not self.game_over:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > self.cols - len(self.stone[0]):
                new_x = self.cols - len(self.stone[0])
            if not self.check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x

    def instant_drop(self):
        if not self.game_over:
            while not self.drop(manual=True):
                pass

    def remove_row(self, board, row):
        del board[row]
        return [[0 for _ in range(self.cols)]] + board

    @staticmethod
    def check_collision(board, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False

    @staticmethod
    def rotate_clockwise(shape):
        return [
            [shape[y][x] for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)
        ]

    @staticmethod
    def join_matrices(mat1, mat2, mat2_off):
        off_x, off_y = mat2_off
        print("off_y:", off_y)
        for cy, row in enumerate(mat2):
            for cx, val in enumerate(row):
                try:
                    mat1[cy + off_y - 1][cx + off_x] += val
                except IndexError as e:
                    print(cy, off_y, cx, off_x)
                    print(cy + off_y - 1, cx + off_x)
                    raise e
        return mat1