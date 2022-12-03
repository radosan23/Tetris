import numpy as np


class Block:
    width = 10

    def __init__(self, b_type, b_state=0):
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
        self.static = False

    def rotate_block(self):
        self.state = (self.state + 1) % len(self.coord)

    def move_right(self):
        self.coord = [[x + 1 for x in st] for st in self.coord]

    def move_left(self):
        self.coord = [[x - 1 for x in st] for st in self.coord]

    def move_down(self):
        self.coord = [[x + Block.width for x in st] for st in self.coord]


class Board:

    def __init__(self, size):
        self.m = size[0]
        self.n = size[1]
        self.curr_block = Block('')
        self.array = None
        self.set_array()

    def set_array(self):
        self.array = np.array([['0 ' if (row * self.m + col in self.curr_block.coord[self.curr_block.state]) else '- '
                              for col in range(self.m)]
                              for row in range(self.n)])

    def add_block(self, block):
        self.curr_block = block
        self.set_array()

    def move_block(self, cmd):
        if not self.curr_block.static:
            if cmd == 'right' and not self.restricted(cmd):
                self.curr_block.move_right()
            elif cmd == 'left' and not self.restricted(cmd):
                self.curr_block.move_left()
            elif cmd == 'rotate' and not self.restricted(cmd):
                self.curr_block.rotate_block()
            self.curr_block.move_down()
            self.set_array()
            self.check_d_border()

    def restricted(self, cmd):
        b_field = self.curr_block.coord[self.curr_block.state]
        next_rot = self.curr_block.coord[(self.curr_block.state + 1) % len(self.curr_block.coord)]
        if cmd == 'right' and any(x for x in b_field if x % self.m == self.m - 1):
            return True
        if cmd == 'left' and any(x for x in b_field if x % self.m == 0):
            return True
        if cmd == 'rotate' and any(x for x in next_rot if x % self.m == self.m - 1) \
                and any(x for x in next_rot if x % self.m == 0):
            return True
        return False

    def check_d_border(self):
        b_field = self.curr_block.coord[self.curr_block.state]
        if any(x for x in b_field if x // self.m == self.n - 1):
            self.curr_block.static = True

    def print_board(self):
        print()
        for row in self.array:
            print(''.join(cell for cell in row).strip())


def main():
    block_type = input()
    size = [int(x) for x in input().split()]
    block = Block(block_type)
    board = Board(size)
    board.print_board()
    board.add_block(block)
    board.print_board()
    while True:
        cmd = input()
        if cmd == 'exit':
            break
        board.move_block(cmd)
        board.print_board()


if __name__ == '__main__':
    main()
