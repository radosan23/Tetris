from collections import deque
import numpy as np
from os import system
import random


class Block:

    def __init__(self, b_type, width, b_state=0):
        types = {'O': [[4, 14, 15, 5]],
                 'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
                 'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
                 'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
                 'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
                 'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
                 'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]],
                 '': [[]]}
        self.type = b_type
        self.state = b_state
        self.coord = types[self.type]
        self.width = width
        self.static = False
        self.freezing = False

    def rotate_block(self):
        self.state = (self.state + 1) % len(self.coord)

    def move_right(self):
        self.coord = [[x + 1 for x in st] for st in self.coord]

    def move_left(self):
        self.coord = [[x - 1 for x in st] for st in self.coord]

    def move_down(self):
        self.coord = [[x + self.width for x in st] for st in self.coord]


class Board:
    symbols = ['O', 'I', 'S', 'Z', 'L', 'J', 'T']

    def __init__(self, size):
        self.m = 10
        self.n = size
        self.blocks = []
        self.curr_block = Block('', self.m)
        self.array = None
        self.frozen = set()
        self.set_array()
        self.queue = deque(random.choices(Board.symbols, k=2))
        self.changes = 3
        self.autodown = False
        self.rem_rows = 0
        self.g_over = False

    @staticmethod
    def get_height():
        while True:
            u_input = input('enter board height (6-100): ')
            try:
                if int(u_input) in range(6, 101):
                    return int(u_input)
            except ValueError:
                pass
            print('wrong value: enter integer from 6 to 100: ')

    def set_array(self):
        all_blocks = list(self.frozen)
        if not self.curr_block.static:
            all_blocks.extend(self.curr_block.coord[self.curr_block.state])
        self.array = np.array([['0 ' if (row * self.m + col in all_blocks) else '- '
                              for col in range(self.m)]
                              for row in range(self.n)])

    def add_block(self):
        b_type = self.queue.popleft()
        self.queue.append(random.choice(Board.symbols))
        self.blocks.append(Block(b_type, self.m))
        self.curr_block = self.blocks[-1]
        self.set_array()

    def move_block(self, cmd):
        if not self.curr_block.static:
            if not self.autodown and not self.curr_block.freezing:
                self.curr_block.move_down()
            if cmd == 'r' and not self.restricted(cmd):
                self.curr_block.move_right()
            elif cmd == 'l' and not self.restricted(cmd):
                self.curr_block.move_left()
            elif cmd == 'o' and not self.restricted(cmd):
                self.curr_block.rotate_block()
            elif cmd == 'd' and self.autodown and not self.curr_block.freezing:
                self.curr_block.move_down()
            self.set_array()

    def remove_rows(self):
        for row in range(self.n):
            if len([cell for cell in self.array[row] if cell == '0 ']) == self.m:
                self.rem_rows += 1
                for x in range(self.m):
                    self.frozen.remove(row * self.m + x)
                self.frozen = {x + self.m if (x // self.m < row) else x for x in self.frozen}
        self.set_array()

    def restricted(self, cmd):
        b_field = self.curr_block.coord[self.curr_block.state]
        next_rot = self.curr_block.coord[(self.curr_block.state + 1) % len(self.curr_block.coord)]
        if cmd == 'r' and (any(x for x in b_field if x % self.m == self.m - 1)
                           or any(x for x in b_field if x+1 in self.frozen)):
            return True
        if cmd == 'l' and (any(x for x in b_field if x % self.m == 0)
                           or any(x for x in b_field if x-1 in self.frozen)):
            return True
        if cmd == 'o' and (any(x for x in next_rot if x % self.m == self.m - 1)
                           and any(x for x in next_rot if x % self.m == 0)
                           or any(x for x in next_rot if x in self.frozen)):
            return True
        return False

    def check_d_border(self):
        b_field = self.curr_block.coord[self.curr_block.state]
        below_piece = [x + self.m for x in b_field]
        if [x for x in b_field if x // self.m == self.n - 1] or [x for x in below_piece if x in self.frozen]:
            if self.curr_block.freezing:
                self.curr_block.static = True
                self.frozen.update(b_field)
            self.curr_block.freezing = True
        else:
            self.curr_block.freezing = False

    def change_next(self):
        if self.changes > 0:
            self.queue.popleft()
            self.queue.append(random.choice(Board.symbols))
            self.changes -= 1

    def print_board(self):
        system('cls')
        print()
        print('next block: ', self.queue[0], '    changes: ', self.changes)
        print()
        for row in self.array:
            print(''.join(cell for cell in row).strip())
        print()

    def game_over(self):
        if [x for x in self.frozen if x < self.m]:
            print('Game Over!')
            input('press enter')
            return True
        return False


def main():
    size = Board.get_height()
    board = Board(size)
    board.add_block()
    board.print_board()
    while True:
        if board.game_over():
            break
        print('choose: x (exit) -- l (left) -- r (right) -- o (rotate) -- c (change)')
        cmd = input()
        if cmd == 'x':
            break
        if cmd == 'c':
            board.change_next()
        else:
            board.move_block(cmd)
            board.check_d_border()
        if board.curr_block.static:
            board.remove_rows()
            board.add_block()
            board.check_d_border()
        board.print_board()


if __name__ == '__main__':
    main()
